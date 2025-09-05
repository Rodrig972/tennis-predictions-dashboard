import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Alert,
  Dimensions
} from 'react-native';
import { Card, Title, Paragraph, ActivityIndicator, Button } from 'react-native-paper';
// import { PieChart, BarChart } from 'react-native-chart-kit';
import * as Animatable from 'react-native-animatable';
import ApiService from '../services/ApiService';

const { width } = Dimensions.get('window');

const DashboardScreen = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState(false);

  useEffect(() => {
    loadDashboardData();
    checkApiConnection();
  }, []);

  const checkApiConnection = async () => {
    const isConnected = await ApiService.checkConnection();
    setConnectionStatus(isConnected);
  };

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await ApiService.getDashboardStats();
      setStats(data);
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de charger les données du dashboard');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    await checkApiConnection();
    setRefreshing(false);
  };

  const getConfidenceData = () => {
    if (!stats) return [];
    
    return [
      {
        name: 'Haute (>70%)',
        count: stats.high_confidence || 0,
        color: '#4CAF50',
        legendFontColor: '#7F7F7F',
        legendFontSize: 12,
      },
      {
        name: 'Moyenne (50-70%)',
        count: stats.medium_confidence || 0,
        color: '#FF9800',
        legendFontColor: '#7F7F7F',
        legendFontSize: 12,
      },
      {
        name: 'Faible (<50%)',
        count: stats.low_confidence || 0,
        color: '#F44336',
        legendFontColor: '#7F7F7F',
        legendFontSize: 12,
      },
    ];
  };

  const getTournamentData = () => {
    if (!stats || !stats.tournaments) return { labels: [], datasets: [{ data: [] }] };
    
    const tournaments = Object.entries(stats.tournaments).slice(0, 5);
    return {
      labels: tournaments.map(([name]) => name.substring(0, 8)),
      datasets: [{
        data: tournaments.map(([, count]) => count)
      }]
    };
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>Chargement du dashboard...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Status de connexion */}
      <Animatable.View animation="fadeInDown" duration={800}>
        <Card style={[styles.card, connectionStatus ? styles.connectedCard : styles.disconnectedCard]}>
          <Card.Content>
            <View style={styles.statusRow}>
              <Text style={styles.statusText}>
                {connectionStatus ? '🟢 API Connectée' : '🔴 API Déconnectée'}
              </Text>
              <Button mode="outlined" onPress={checkApiConnection} compact>
                Tester
              </Button>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Statistiques principales */}
      <Animatable.View animation="fadeInUp" duration={800} delay={200}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>📊 Statistiques Globales</Title>
            <View style={styles.statsGrid}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats?.total_tournaments || 0}</Text>
                <Text style={styles.statLabel}>Tournois</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats?.total_matches || 0}</Text>
                <Text style={styles.statLabel}>Matchs</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats?.average_confidence?.toFixed(1) || 0}%</Text>
                <Text style={styles.statLabel}>Confiance Moy.</Text>
              </View>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Statistiques de confiance */}
      {stats && (
        <Animatable.View animation="fadeInLeft" duration={800} delay={400}>
          <Card style={styles.card}>
            <Card.Content>
              <Title style={styles.cardTitle}>🎯 Répartition par Confiance</Title>
              <View style={styles.statsContainer}>
                <View style={styles.statItem}>
                  <Text style={[styles.statValue, {color: '#4CAF50'}]}>
                    {stats.high_confidence || 0}
                  </Text>
                  <Text style={styles.statLabel}>Haute (&gt;70%)</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={[styles.statValue, {color: '#FF9800'}]}>
                    {stats.medium_confidence || 0}
                  </Text>
                  <Text style={styles.statLabel}>Moyenne (50-70%)</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={[styles.statValue, {color: '#F44336'}]}>
                    {stats.low_confidence || 0}
                  </Text>
                  <Text style={styles.statLabel}>Faible (&lt;50%)</Text>
                </View>
              </View>
            </Card.Content>
          </Card>
        </Animatable.View>
      )}

      {/* Top Tournois */}
      {stats && stats.tournaments && (
        <Animatable.View animation="fadeInRight" duration={800} delay={600}>
          <Card style={styles.card}>
            <Card.Content>
              <Title style={styles.cardTitle}>🏆 Top Tournois</Title>
              <View style={styles.tournamentContainer}>
                {Object.entries(stats.tournaments).slice(0, 5).map(([name, count], index) => (
                  <View key={index} style={styles.tournamentItem}>
                    <Text style={styles.tournamentName}>{name}</Text>
                    <View style={styles.tournamentBar}>
                      <View 
                        style={[
                          styles.tournamentProgress, 
                          { width: `${(count / Math.max(...Object.values(stats.tournaments))) * 100}%` }
                        ]} 
                      />
                      <Text style={styles.tournamentCount}>{count}</Text>
                    </View>
                  </View>
                ))}
              </View>
            </Card.Content>
          </Card>
        </Animatable.View>
      )}

      {/* Dernières prédictions */}
      <Animatable.View animation="fadeInUp" duration={800} delay={800}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>⚡ Dernières Prédictions</Title>
            {stats?.recent_predictions?.map((prediction, index) => (
              <View key={index} style={styles.predictionItem}>
                <Text style={styles.predictionMatch}>
                  {prediction.player_a} vs {prediction.player_b}
                </Text>
                <Text style={styles.predictionTournament}>{prediction.tournament}</Text>
                <View style={styles.predictionStats}>
                  <Text style={[styles.confidence, { 
                    color: prediction.confidence > 70 ? '#4CAF50' : 
                           prediction.confidence > 50 ? '#FF9800' : '#F44336' 
                  }]}>
                    {prediction.confidence.toFixed(1)}%
                  </Text>
                </View>
              </View>
            ))}
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
  card: {
    marginBottom: 16,
    elevation: 4,
  },
  connectedCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#4CAF50',
  },
  disconnectedCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#F44336',
  },
  statusRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#2196F3',
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  predictionItem: {
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  predictionMatch: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  predictionTournament: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  predictionStats: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 4,
  },
  confidence: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 10,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  tournamentContainer: {
    marginTop: 10,
  },
  tournamentItem: {
    marginBottom: 12,
  },
  tournamentName: {
    fontSize: 14,
    fontWeight: '500',
    marginBottom: 4,
  },
  tournamentBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    height: 24,
    position: 'relative',
  },
  tournamentProgress: {
    backgroundColor: '#2196F3',
    height: '100%',
    borderRadius: 8,
    minWidth: 20,
  },
  tournamentCount: {
    position: 'absolute',
    right: 8,
    fontSize: 12,
    fontWeight: 'bold',
    color: '#333',
  },
});

export default DashboardScreen;
