import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider } from 'react-native-paper';
import { MaterialIcons } from '@expo/vector-icons';

import DashboardScreen from './src/screens/DashboardScreen';
import PredictionsScreen from './src/screens/PredictionsScreen';
import MatchDetailScreen from './src/screens/MatchDetailScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const PredictionsStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="PredictionsList" 
      component={PredictionsScreen}
      options={{ title: 'Prédictions Tennis' }}
    />
    <Stack.Screen 
      name="MatchDetail" 
      component={MatchDetailScreen}
      options={{ title: 'Détail du Match' }}
    />
  </Stack.Navigator>
);

const MainTabs = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      tabBarIcon: ({ focused, color, size }) => {
        let iconName;
        
        if (route.name === 'Dashboard') {
          iconName = 'dashboard';
        } else if (route.name === 'Predictions') {
          iconName = 'sports-tennis';
        } else if (route.name === 'Settings') {
          iconName = 'settings';
        }
        
        return <MaterialIcons name={iconName} size={size} color={color} />;
      },
      tabBarActiveTintColor: '#2196F3',
      tabBarInactiveTintColor: 'gray',
      headerShown: false,
    })}
  >
    <Tab.Screen 
      name="Dashboard" 
      component={DashboardScreen}
      options={{ tabBarLabel: 'Tableau de Bord' }}
    />
    <Tab.Screen 
      name="Predictions" 
      component={PredictionsStack}
      options={{ tabBarLabel: 'Prédictions' }}
    />
    <Tab.Screen 
      name="Settings" 
      component={SettingsScreen}
      options={{ tabBarLabel: 'Paramètres' }}
    />
  </Tab.Navigator>
);

export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <MainTabs />
      </NavigationContainer>
    </PaperProvider>
  );
}
