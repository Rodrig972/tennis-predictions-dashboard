import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  Alert
} from 'react-native';
import { Card, Title, Chip, ActivityIndicator, Searchbar } from 'react-native-paper';
import * as Animatable from 'react-native-animatable';
import ApiService from '../services/ApiService';

const PredictionsScreen = ({ navigation }) => {
  const [predictions, setPredictions] = useState([]);
  const [filteredPredictions, setFilteredPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');

  useEffect(() => {
    loadPredictions();
  }, []);

  useEffect(() => {
    filterPredictions();
  }, [predictions, searchQuery, selectedFilter]);

  const loadPredictions = async () => {
    try {
      setLoading(true);
      const data = await ApiService.getPredictions();
      setPredictions(data.predictions || []);
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de charger les prédictions');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadPredictions();
    setRefreshing(false);
  };

  const filterPredictions = () => {
    let filtered = predictions;

    // Filtrer par recherche
    if (searchQuery) {
      filtered = filtered.filter(pred =>
        pred.player_a.toLowerCase().includes(searchQuery.toLowerCase()) ||
        pred.player_b.toLowerCase().includes(searchQuery.toLowerCase()) ||
        pred.tournament.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Filtrer par confiance
    if (selectedFilter !== 'all') {
      filtered = filtered.filter(pred => {
        if (selectedFilter === 'high') return pred.confidence > 70;
        if (selectedFilter === 'medium') return pred.confidence >= 50 && pred.confidence <= 70;
        if (selectedFilter === 'low') return pred.confidence < 50;
        return true;
      });
    }

    setFilteredPredictions(filtered);
  };

  const getConfidenceColor = (confidence) => {
    if (confidence > 70) return '#4CAF50';
    if (confidence >= 50) return '#FF9800';
    return '#F44336';
  };

  const getConfidenceBadge = (confidence) => {
    if (confidence > 70) return 'HAUTE';
    if (confidence >= 50) return 'MOYENNE';
    return 'FAIBLE';
  };

  const renderPredictionItem = ({ item, index }) => (
    <Animatable.View
      animation="fadeInUp"
      duration={600}
      delay={index * 100}
    >
      <TouchableOpacity
        onPress={() => navigation.navigate('MatchDetail', { 
          tournament: item.tournament, 
          match: `${item.player_a} vs ${item.player_b}` 
        })}
      >
        <Card style={styles.predictionCard}>
          <Card.Content>
            <View style={styles.cardHeader}>
              <Text style={styles.tournament}>{item.tournament}</Text>
              <Chip
                mode="flat"
                style={[styles.confidenceChip, { backgroundColor: getConfidenceColor(item.confidence) + '20' }]}
                textStyle={[styles.confidenceText, { color: getConfidenceColor(item.confidence) }]}
              >
                {getConfidenceBadge(item.confidence)}
              </Chip>
            </View>

            <View style={styles.matchContainer}>
              <View style={styles.playerContainer}>
                <Text style={[
                  styles.playerName,
                  item.favorite === item.player_a && styles.favoritePlayer
                ]}>
                  {item.player_a}
                </Text>
                <View style={styles.probabilityContainer}>
                  <Text style={styles.probabilityText}>
                    {item.probability_a.toFixed(1)}%
                  </Text>
                  <View style={[
                    styles.probabilityBar,
                    { width: `${item.probability_a}%`, backgroundColor: getConfidenceColor(item.confidence) }
                  ]} />
                </View>
                <Text style={styles.oddsText}>Cote: {item.odds_a.toFixed(2)}</Text>
              </View>

              <Text style={styles.vsText}>VS</Text>

              <View style={styles.playerContainer}>
                <Text style={[
                  styles.playerName,
                  item.favorite === item.player_b && styles.favoritePlayer
                ]}>
                  {item.player_b}
                </Text>
                <View style={styles.probabilityContainer}>
                  <Text style={styles.probabilityText}>
                    {item.probability_b.toFixed(1)}%
                  </Text>
                  <View style={[
                    styles.probabilityBar,
                    { width: `${item.probability_b}%`, backgroundColor: getConfidenceColor(item.confidence) }
                  ]} />
                </View>
                <Text style={styles.oddsText}>Cote: {item.odds_b.toFixed(2)}</Text>
              </View>
            </View>

            <View style={styles.cardFooter}>
              <Text style={styles.favoriteText}>
                🏆 Favori: {item.favorite}
              </Text>
              <Text style={[styles.confidenceValue, { color: getConfidenceColor(item.confidence) }]}>
                {item.confidence.toFixed(1)}%
              </Text>
            </View>
          </Card.Content>
        </Card>
      </TouchableOpacity>
    </Animatable.View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>Chargement des prédictions...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Barre de recherche */}
      <Searchbar
        placeholder="Rechercher joueurs ou tournois..."
        onChangeText={setSearchQuery}
        value={searchQuery}
        style={styles.searchBar}
      />

      {/* Filtres */}
      <View style={styles.filtersContainer}>
        <TouchableOpacity
          onPress={() => setSelectedFilter('all')}
          style={[styles.filterChip, selectedFilter === 'all' && styles.activeFilter]}
        >
          <Text style={[styles.filterText, selectedFilter === 'all' && styles.activeFilterText]}>
            Tous
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() => setSelectedFilter('high')}
          style={[styles.filterChip, selectedFilter === 'high' && styles.activeFilter]}
        >
          <Text style={[styles.filterText, selectedFilter === 'high' && styles.activeFilterText]}>
            Haute Confiance
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() => setSelectedFilter('medium')}
          style={[styles.filterChip, selectedFilter === 'medium' && styles.activeFilter]}
        >
          <Text style={[styles.filterText, selectedFilter === 'medium' && styles.activeFilterText]}>
            Moyenne
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() => setSelectedFilter('low')}
          style={[styles.filterChip, selectedFilter === 'low' && styles.activeFilter]}
        >
          <Text style={[styles.filterText, selectedFilter === 'low' && styles.activeFilterText]}>
            Faible
          </Text>
        </TouchableOpacity>
      </View>

      {/* Liste des prédictions */}
      <FlatList
        data={filteredPredictions}
        renderItem={renderPredictionItem}
        keyExtractor={(item, index) => `${item.tournament}-${index}`}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  searchBar: {
    margin: 16,
    elevation: 4,
  },
  filtersContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingBottom: 16,
    justifyContent: 'space-around',
  },
  filterChip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: '#e0e0e0',
  },
  activeFilter: {
    backgroundColor: '#2196F3',
  },
  filterText: {
    fontSize: 12,
    color: '#666',
  },
  activeFilterText: {
    color: 'white',
  },
  listContainer: {
    paddingHorizontal: 16,
  },
  predictionCard: {
    marginBottom: 16,
    elevation: 4,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  tournament: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2196F3',
    flex: 1,
  },
  confidenceChip: {
    height: 24,
  },
  confidenceText: {
    fontSize: 10,
    fontWeight: 'bold',
  },
  matchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  playerContainer: {
    flex: 1,
  },
  playerName: {
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 8,
  },
  favoritePlayer: {
    color: '#2196F3',
  },
  probabilityContainer: {
    alignItems: 'center',
    marginBottom: 4,
  },
  probabilityText: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  probabilityBar: {
    height: 4,
    borderRadius: 2,
    marginBottom: 4,
  },
  oddsText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  vsText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#666',
    marginHorizontal: 16,
  },
  cardFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  favoriteText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  confidenceValue: {
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default PredictionsScreen;
