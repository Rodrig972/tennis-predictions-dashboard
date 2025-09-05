import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Alert,
  Dimensions
} from 'react-native';
import { Card, Title, ActivityIndicator, Chip } from 'react-native-paper';
// import { PieChart, ProgressChart } from 'react-native-chart-kit';
import * as Animatable from 'react-native-animatable';
import ApiService from '../services/ApiService';

const { width } = Dimensions.get('window');

const MatchDetailScreen = ({ route }) => {
  const { tournament, match } = route.params;
  const [matchDetail, setMatchDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMatchDetail();
  }, []);

  const loadMatchDetail = async () => {
    try {
      setLoading(true);
      const data = await ApiService.getMatchDetail(tournament, match);
      setMatchDetail(data);
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de charger les détails du match');
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence > 70) return '#4CAF50';
    if (confidence >= 50) return '#FF9800';
    return '#F44336';
  };

  const getProbabilityData = () => {
    if (!matchDetail) return [];
    
    return [
      {
        name: matchDetail.player_a,
        probability: matchDetail.probability_a,
        color: '#2196F3',
        legendFontColor: '#7F7F7F',
        legendFontSize: 12,
      },
      {
        name: matchDetail.player_b,
        probability: matchDetail.probability_b,
        color: '#FF9800',
        legendFontColor: '#7F7F7F',
        legendFontSize: 12,
      },
    ];
  };

  const getProgressData = () => {
    if (!matchDetail) return { data: [] };
    
    return {
      data: [matchDetail.confidence / 100]
    };
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>Chargement des détails...</Text>
      </View>
    );
  }

  if (!matchDetail) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Aucun détail disponible pour ce match</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* En-tête du match */}
      <Animatable.View animation="fadeInDown" duration={800}>
        <Card style={styles.headerCard}>
          <Card.Content>
            <Title style={styles.tournamentTitle}>{matchDetail.tournament}</Title>
            <View style={styles.matchHeader}>
              <View style={styles.playerSection}>
                <Text style={[
                  styles.playerName,
                  matchDetail.favorite === matchDetail.player_a && styles.favoritePlayer
                ]}>
                  {matchDetail.player_a}
                </Text>
                <Text style={styles.probabilityText}>
                  {matchDetail.probability_a.toFixed(1)}%
                </Text>
                <Text style={styles.oddsText}>
                  Cote: {matchDetail.odds_a.toFixed(2)}
                </Text>
              </View>
              
              <View style={styles.vsContainer}>
                <Text style={styles.vsText}>VS</Text>
                <Chip
                  mode="flat"
                  style={[styles.confidenceChip, { backgroundColor: getConfidenceColor(matchDetail.confidence) + '20' }]}
                  textStyle={[styles.confidenceText, { color: getConfidenceColor(matchDetail.confidence) }]}
                >
                  {matchDetail.confidence.toFixed(1)}%
                </Chip>
              </View>
              
              <View style={styles.playerSection}>
                <Text style={[
                  styles.playerName,
                  matchDetail.favorite === matchDetail.player_b && styles.favoritePlayer
                ]}>
                  {matchDetail.player_b}
                </Text>
                <Text style={styles.probabilityText}>
                  {matchDetail.probability_b.toFixed(1)}%
                </Text>
                <Text style={styles.oddsText}>
                  Cote: {matchDetail.odds_b.toFixed(2)}
                </Text>
              </View>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Probabilités des joueurs */}
      <Animatable.View animation="fadeInLeft" duration={800} delay={200}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>📊 Probabilités de Victoire</Title>
            <View style={styles.probabilityContainer}>
              <View style={styles.playerProbability}>
                <Text style={styles.playerName}>{matchDetail.player_a}</Text>
                <View style={styles.probabilityBar}>
                  <View 
                    style={[
                      styles.probabilityFill, 
                      { width: `${matchDetail.probability_a}%`, backgroundColor: '#4CAF50' }
                    ]} 
                  />
                </View>
                <Text style={[styles.probabilityText, {color: '#4CAF50'}]}>
                  {matchDetail.probability_a.toFixed(1)}%
                </Text>
              </View>
              <View style={styles.playerProbability}>
                <Text style={styles.playerName}>{matchDetail.player_b}</Text>
                <View style={styles.probabilityBar}>
                  <View 
                    style={[
                      styles.probabilityFill, 
                      { width: `${matchDetail.probability_b}%`, backgroundColor: '#F44336' }
                    ]} 
                  />
                </View>
                <Text style={[styles.probabilityText, {color: '#F44336'}]}>
                  {matchDetail.probability_b.toFixed(1)}%
                </Text>
              </View>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Niveau de confiance */}
      <Animatable.View animation="fadeInRight" duration={800} delay={400}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>🎯 Niveau de Confiance</Title>
            <View style={styles.confidenceContainer}>
              <View style={styles.confidenceCircle}>
                <View 
                  style={[
                    styles.confidenceProgress,
                    { 
                      backgroundColor: getConfidenceColor(matchDetail.confidence),
                      width: `${matchDetail.confidence}%`
                    }
                  ]}
                />
              </View>
              <Text style={[styles.confidenceValue, { color: getConfidenceColor(matchDetail.confidence) }]}>
                {matchDetail.confidence.toFixed(1)}%
              </Text>
              <Text style={styles.confidenceLabel}>
                {matchDetail.confidence > 70 ? 'Haute Confiance' : 
                 matchDetail.confidence > 50 ? 'Confiance Moyenne' : 'Faible Confiance'}
              </Text>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Analyse détaillée */}
      <Animatable.View animation="fadeInUp" duration={800} delay={600}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>🔍 Analyse Détaillée</Title>
            
            <View style={styles.analysisSection}>
              <Text style={styles.analysisTitle}>🏆 Favori Prédit</Text>
              <Text style={styles.favoriteText}>{matchDetail.favorite}</Text>
            </View>

            <View style={styles.analysisSection}>
              <Text style={styles.analysisTitle}>💰 Valeur des Cotes</Text>
              <View style={styles.oddsComparison}>
                <View style={styles.oddsItem}>
                  <Text style={styles.oddsPlayer}>{matchDetail.player_a}</Text>
                  <Text style={styles.oddsValue}>{matchDetail.odds_a.toFixed(2)}</Text>
                </View>
                <View style={styles.oddsItem}>
                  <Text style={styles.oddsPlayer}>{matchDetail.player_b}</Text>
                  <Text style={styles.oddsValue}>{matchDetail.odds_b.toFixed(2)}</Text>
                </View>
              </View>
            </View>

            <View style={styles.analysisSection}>
              <Text style={styles.analysisTitle}>📈 Recommandation</Text>
              <Text style={styles.recommendationText}>
                {matchDetail.confidence > 70 
                  ? `Prédiction très fiable. ${matchDetail.favorite} est fortement favori.`
                  : matchDetail.confidence > 50
                  ? `Prédiction modérée. Match équilibré avec un léger avantage pour ${matchDetail.favorite}.`
                  : `Prédiction incertaine. Match très ouvert entre les deux joueurs.`
                }
              </Text>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Informations techniques */}
      <Animatable.View animation="fadeInUp" duration={800} delay={800}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>⚙️ Informations Techniques</Title>
            
            <View style={styles.techInfo}>
              <View style={styles.techItem}>
                <Text style={styles.techLabel}>Algorithme utilisé:</Text>
                <Text style={styles.techValue}>Machine Learning (XGBoost)</Text>
              </View>
              
              <View style={styles.techItem}>
                <Text style={styles.techLabel}>Données analysées:</Text>
                <Text style={styles.techValue}>35+ caractéristiques</Text>
              </View>
              
              <View style={styles.techItem}>
                <Text style={styles.techLabel}>Base d'entraînement:</Text>
                <Text style={styles.techValue}>59,636 matchs historiques</Text>
              </View>
              
              <View style={styles.techItem}>
                <Text style={styles.techLabel}>Précision moyenne:</Text>
                <Text style={styles.techValue}>~75%</Text>
              </View>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 16,
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
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  errorText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  headerCard: {
    marginBottom: 16,
    elevation: 6,
  },
  tournamentTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2196F3',
    textAlign: 'center',
    marginBottom: 16,
  },
  matchHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  playerSection: {
    flex: 1,
    alignItems: 'center',
  },
  playerName: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 8,
  },
  favoritePlayer: {
    color: '#2196F3',
  },
  probabilityText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 4,
  },
  oddsText: {
    fontSize: 14,
    color: '#666',
  },
  vsContainer: {
    alignItems: 'center',
    marginHorizontal: 16,
  },
  vsText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#666',
    marginBottom: 8,
  },
  confidenceChip: {
    height: 28,
  },
  confidenceText: {
    fontSize: 12,
    fontWeight: 'bold',
  },
  card: {
    marginBottom: 16,
    elevation: 4,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#2196F3',
  },
  confidenceContainer: {
    alignItems: 'center',
    marginVertical: 20,
  },
  confidenceCircle: {
    width: 200,
    height: 20,
    backgroundColor: '#f0f0f0',
    borderRadius: 10,
    marginBottom: 10,
  },
  confidenceProgress: {
    height: '100%',
    borderRadius: 10,
    minWidth: 20,
  },
  confidenceValue: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  confidenceLabel: {
    fontSize: 14,
    color: '#666',
  },
  probabilityContainer: {
    marginTop: 10,
  },
  playerProbability: {
    marginBottom: 20,
  },
  playerName: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  probabilityBar: {
    width: '100%',
    height: 24,
    backgroundColor: '#f0f0f0',
    borderRadius: 12,
    marginBottom: 8,
  },
  probabilityFill: {
    height: '100%',
    borderRadius: 12,
    minWidth: 20,
  },
  probabilityText: {
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  analysisSection: {
    marginBottom: 16,
  },
  analysisTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#333',
  },
  favoriteText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  oddsComparison: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  oddsItem: {
    alignItems: 'center',
  },
  oddsPlayer: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  oddsValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FF9800',
  },
  recommendationText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  techInfo: {
    backgroundColor: '#f8f9fa',
    padding: 12,
    borderRadius: 8,
  },
  techItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  techLabel: {
    fontSize: 14,
    color: '#666',
  },
  techValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
});

export default MatchDetailScreen;
