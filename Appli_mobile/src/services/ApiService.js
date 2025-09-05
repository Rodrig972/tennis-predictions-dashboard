import axios from 'axios';

class ApiService {
  constructor() {
    // URL de base de votre API Flask
    // Pour l'émulateur Android, utilisez 10.0.2.2 au lieu de 127.0.0.1
    // Pour un appareil physique ou Expo Go, utilisez l'IP de votre machine
    this.baseURL = 'http://192.168.1.20:5000';
    this.api = axios.create({
      baseURL: this.baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Récupérer toutes les prédictions
  async getPredictions() {
    try {
      console.log('Tentative de connexion à:', this.baseURL + '/api/predictions');
      const response = await this.api.get('/api/predictions');
      console.log('Réponse API reçue:', response.data.length, 'matchs');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des prédictions:', error.message);
      console.error('URL tentée:', this.baseURL + '/api/predictions');
      throw error;
    }
  }

  // Récupérer les statistiques du dashboard
  async getDashboardStats() {
    try {
      const response = await this.api.get('/api/dashboard');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des stats:', error);
      throw error;
    }
  }

  // Récupérer les détails d'un match
  async getMatchDetail(tournamentName, matchName) {
    try {
      const response = await this.api.get(`/api/match/${encodeURIComponent(tournamentName)}/${encodeURIComponent(matchName)}`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération du détail du match:', error);
      throw error;
    }
  }

  // Récupérer les prédictions par tournoi
  async getPredictionsByTournament(tournamentName) {
    try {
      const response = await this.api.get(`/api/tournament/${encodeURIComponent(tournamentName)}`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des prédictions du tournoi:', error);
      throw error;
    }
  }

  // Faire une nouvelle prédiction
  async makePrediction(player1, player2, surface = 'Hard', tournament = 'ATP250') {
    try {
      const response = await this.api.post('/api/predict', {
        player1,
        player2,
        surface,
        tournament
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la prédiction:', error);
      throw error;
    }
  }

  // Vérifier la connexion à l'API
  async checkConnection() {
    try {
      const response = await this.api.get('/api/health');
      return response.status === 200;
    } catch (error) {
      console.error('Connexion API échouée:', error);
      return false;
    }
  }
}

export default new ApiService();
