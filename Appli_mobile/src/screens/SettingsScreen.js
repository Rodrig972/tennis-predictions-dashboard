import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Alert,
  Switch,
  TouchableOpacity
} from 'react-native';
import { Card, Title, List, Button, TextInput, Divider } from 'react-native-paper';
import * as Animatable from 'react-native-animatable';
import ApiService from '../services/ApiService';

const SettingsScreen = () => {
  const [apiUrl, setApiUrl] = useState('http://127.0.0.1:5000');
  const [notifications, setNotifications] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState(false);

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    const isConnected = await ApiService.checkConnection();
    setConnectionStatus(isConnected);
  };

  const testConnection = async () => {
    try {
      // Mettre à jour l'URL de base de l'API
      ApiService.baseURL = apiUrl;
      ApiService.api.defaults.baseURL = apiUrl;
      
      const isConnected = await ApiService.checkConnection();
      setConnectionStatus(isConnected);
      
      Alert.alert(
        'Test de Connexion',
        isConnected ? 'Connexion réussie ✅' : 'Connexion échouée ❌',
        [{ text: 'OK' }]
      );
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de tester la connexion');
    }
  };

  const resetSettings = () => {
    Alert.alert(
      'Réinitialiser les Paramètres',
      'Êtes-vous sûr de vouloir réinitialiser tous les paramètres ?',
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: 'Réinitialiser',
          style: 'destructive',
          onPress: () => {
            setApiUrl('http://127.0.0.1:5000');
            setNotifications(true);
            setAutoRefresh(false);
            setDarkMode(false);
            Alert.alert('Succès', 'Paramètres réinitialisés');
          }
        }
      ]
    );
  };

  const clearCache = () => {
    Alert.alert(
      'Vider le Cache',
      'Cette action supprimera toutes les données mises en cache.',
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: 'Vider',
          style: 'destructive',
          onPress: () => {
            // Ici vous pourriez implémenter la logique de vidage du cache
            Alert.alert('Succès', 'Cache vidé avec succès');
          }
        }
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      {/* Status de connexion */}
      <Animatable.View animation="fadeInDown" duration={800}>
        <Card style={[styles.card, connectionStatus ? styles.connectedCard : styles.disconnectedCard]}>
          <Card.Content>
            <View style={styles.statusContainer}>
              <Text style={styles.statusTitle}>État de la Connexion</Text>
              <Text style={[styles.statusText, { color: connectionStatus ? '#4CAF50' : '#F44336' }]}>
                {connectionStatus ? '🟢 Connecté' : '🔴 Déconnecté'}
              </Text>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Configuration API */}
      <Animatable.View animation="fadeInUp" duration={800} delay={200}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>🔗 Configuration API</Title>
            
            <TextInput
              label="URL de l'API"
              value={apiUrl}
              onChangeText={setApiUrl}
              mode="outlined"
              style={styles.input}
              placeholder="http://127.0.0.1:5000"
            />
            
            <View style={styles.buttonRow}>
              <Button
                mode="contained"
                onPress={testConnection}
                style={styles.testButton}
                icon="wifi"
              >
                Tester Connexion
              </Button>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Préférences */}
      <Animatable.View animation="fadeInUp" duration={800} delay={400}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>⚙️ Préférences</Title>
            
            <List.Item
              title="Notifications Push"
              description="Recevoir des notifications pour les nouvelles prédictions"
              left={props => <List.Icon {...props} icon="bell" />}
              right={() => (
                <Switch
                  value={notifications}
                  onValueChange={setNotifications}
                  color="#2196F3"
                />
              )}
            />
            
            <Divider />
            
            <List.Item
              title="Actualisation Automatique"
              description="Actualiser automatiquement les données toutes les 5 minutes"
              left={props => <List.Icon {...props} icon="refresh" />}
              right={() => (
                <Switch
                  value={autoRefresh}
                  onValueChange={setAutoRefresh}
                  color="#2196F3"
                />
              )}
            />
            
            <Divider />
            
            <List.Item
              title="Mode Sombre"
              description="Utiliser le thème sombre (bientôt disponible)"
              left={props => <List.Icon {...props} icon="theme-light-dark" />}
              right={() => (
                <Switch
                  value={darkMode}
                  onValueChange={setDarkMode}
                  color="#2196F3"
                  disabled={true}
                />
              )}
            />
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Actions */}
      <Animatable.View animation="fadeInUp" duration={800} delay={600}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>🛠️ Actions</Title>
            
            <Button
              mode="outlined"
              onPress={clearCache}
              style={styles.actionButton}
              icon="delete-sweep"
            >
              Vider le Cache
            </Button>
            
            <Button
              mode="outlined"
              onPress={resetSettings}
              style={styles.actionButton}
              icon="restore"
            >
              Réinitialiser les Paramètres
            </Button>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Informations sur l'application */}
      <Animatable.View animation="fadeInUp" duration={800} delay={800}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>ℹ️ À Propos</Title>
            
            <View style={styles.infoSection}>
              <Text style={styles.infoLabel}>Version de l'Application:</Text>
              <Text style={styles.infoValue}>1.0.0</Text>
            </View>
            
            <View style={styles.infoSection}>
              <Text style={styles.infoLabel}>Développé par:</Text>
              <Text style={styles.infoValue}>Tennis Prediction System</Text>
            </View>
            
            <View style={styles.infoSection}>
              <Text style={styles.infoLabel}>Technologie:</Text>
              <Text style={styles.infoValue}>React Native + Expo</Text>
            </View>
            
            <View style={styles.infoSection}>
              <Text style={styles.infoLabel}>API Backend:</Text>
              <Text style={styles.infoValue}>Flask + Machine Learning</Text>
            </View>
            
            <View style={styles.infoSection}>
              <Text style={styles.infoLabel}>Algorithmes ML:</Text>
              <Text style={styles.infoValue}>XGBoost, RandomForest, Gradient Boosting</Text>
            </View>
          </Card.Content>
        </Card>
      </Animatable.View>

      {/* Support */}
      <Animatable.View animation="fadeInUp" duration={800} delay={1000}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>📞 Support</Title>
            
            <Text style={styles.supportText}>
              Pour toute question ou problème technique, consultez la documentation 
              ou contactez l'équipe de développement.
            </Text>
            
            <Button
              mode="contained"
              onPress={() => Alert.alert('Support', 'Fonctionnalité bientôt disponible')}
              style={styles.supportButton}
              icon="help-circle"
            >
              Aide & Documentation
            </Button>
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
  statusContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusTitle: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  statusText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#2196F3',
  },
  input: {
    marginBottom: 16,
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  testButton: {
    flex: 1,
  },
  actionButton: {
    marginBottom: 12,
  },
  infoSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
    paddingVertical: 4,
  },
  infoLabel: {
    fontSize: 14,
    color: '#666',
    flex: 1,
  },
  infoValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    textAlign: 'right',
  },
  supportText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 16,
    textAlign: 'center',
  },
  supportButton: {
    marginTop: 8,
  },
});

export default SettingsScreen;
