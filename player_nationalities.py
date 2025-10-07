#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base de données des nationalités des joueurs de tennis et pays des tournois
"""

# Nationalités des joueurs de tennis (échantillon des joueurs les plus connus)
PLAYER_NATIONALITIES = {
    # Joueurs ATP populaires
    'Djokovic': 'RS',  # Serbie
    'Nadal': 'ES',     # Espagne
    'Federer': 'CH',   # Suisse
    'Alcaraz': 'ES',   # Espagne
    'Medvedev': 'RU',  # Russie
    'Zverev': 'DE',    # Allemagne
    'Tsitsipas': 'GR', # Grèce
    'Rublev': 'RU',    # Russie
    'Sinner': 'IT',    # Italie
    'Berrettini': 'IT', # Italie
    'Thiem': 'AT',     # Autriche
    
    # Joueurs actuels dans les prédictions
    'Halys': 'FR',         # France
    'O\'Connell': 'AU',    # Australie
    'Norrie': 'GB',        # Grande-Bretagne
    'Zhou': 'CN',          # Chine
    'Bergs': 'BE',         # Belgique
    'Shang': 'CN',         # Chine
    'Giron': 'US',         # États-Unis
    'Quinn': 'US',         # États-Unis
    'Sonego': 'IT',        # Italie
    'Cerundolo': 'AR',     # Argentine
    'Misolic': 'AT',       # Autriche
    'Mpetshi Perricard': 'FR', # France
    'Shevchenko': 'KZ',    # Kazakhstan
    'Monfils': 'FR',       # France
    'Atmane': 'DZ',        # Algérie
    'Prizmic': 'HR',       # Croatie
    'Walton': 'AU',        # Australie
    'Korda': 'US',         # États-Unis
    'Mannarino': 'FR',     # France
    'Wu': 'TW',            # Taiwan
    'Vukic': 'AU',         # Australie
    'Goffin': 'BE',        # Belgique
    'Yunchaokete': 'CN',   # Chine
    'Zhang': 'CN',         # Chine
    'Dzumhur': 'BA',       # Bosnie-Herzégovine
    'Etcheverry': 'AR',    # Argentine
    'Cazaux': 'FR',        # France
    'Arnaldi': 'IT',       # Italie
    'Navone': 'AR',        # Argentine
    'Tien': 'US',          # États-Unis
    'Kovacevic': 'AU',     # Australie
    'Nardi': 'IT',         # Italie
    
    # Joueuses WTA actuelles
    'Shnaider': 'RU',      # Russie
    'McNally': 'US',       # États-Unis
    'Krejcikova': 'CZ',    # République tchèque
    'Prozorova': 'UA',     # Ukraine
    'Lamens': 'NL',        # Pays-Bas
    'Maria': 'GR',         # Grèce
    'Cristian': 'RO',      # Roumanie
    'Raducanu': 'GB',      # Grande-Bretagne
    'Haddad Maia': 'BR',   # Brésil
    'Back': 'BE',          # Belgique
    'Boisson': 'FR',       # France
    'Alexandrova': 'RU',   # Russie
    'Joint': 'AU',         # Australie
    'Kenin': 'US',         # États-Unis
    'Siniakova': 'CZ',     # République tchèque
    'Kasatkina': 'RU',     # Russie
    'Tauson': 'DK',        # Danemark
    'Lys': 'DE',           # Allemagne
    'Wawrinka': 'CH',  # Suisse
    'Murray': 'GB',    # Grande-Bretagne
    'Kyrgios': 'AU',   # Australie
    'De Minaur': 'AU', # Australie
    'Fritz': 'US',     # États-Unis
    'Tiafoe': 'US',    # États-Unis
    'Paul': 'US',      # États-Unis
    'Hurkacz': 'PL',   # Pologne
    'Shapovalov': 'CA', # Canada
    'Auger-Aliassime': 'CA', # Canada
    'Norrie': 'GB',    # Grande-Bretagne
    'Ruud': 'NO',      # Norvège
    'Rune': 'DK',      # Danemark
    'Musetti': 'IT',   # Italie
    'Korda': 'US',     # États-Unis
    'Shelton': 'US',   # États-Unis
    'Arnaldi': 'IT',   # Italie
    'Cazaux': 'FR',    # France
    'Tien': 'US',      # États-Unis
    'Navone': 'AR',    # Argentine
    'Kovacevic': 'US', # États-Unis
    'Nardi': 'IT',     # Italie
    
    # Joueuses WTA populaires
    'Swiatek': 'PL',   # Pologne
    'Sabalenka': 'BY', # Biélorussie
    'Gauff': 'US',     # États-Unis
    'Rybakina': 'KZ',  # Kazakhstan
    'Jabeur': 'TN',    # Tunisie
    'Pegula': 'US',    # États-Unis
    'Vondrousova': 'CZ', # République tchèque
    'Ostapenko': 'LV', # Lettonie
    'Keys': 'US',      # États-Unis
    'Krejcikova': 'CZ', # République tchèque
    'Muchova': 'CZ',   # République tchèque
    'Badosa': 'ES',    # Espagne
    'Sakkari': 'GR',   # Grèce
    'Kvitova': 'CZ',   # République tchèque
    'Azarenka': 'BY',  # Biélorussie
    'Halep': 'RO',     # Roumanie
    'Kenin': 'US',     # États-Unis
    'Andreescu': 'CA', # Canada
    'Fernandez': 'CA', # Canada
    'Raducanu': 'GB',  # Grande-Bretagne
    'Trevisan': 'IT',  # Italie
    'Marino': 'CA',    # Canada
    'Alexandrova': 'RU', # Russie
    'Joint': 'AU',     # Australie
    'Boisson': 'FR',   # France
    'Linette': 'PL',   # Pologne
    'Arango': 'CO',    # Colombie
    'Stephens': 'US',  # États-Unis
    'Stefanini': 'BR', # Brésil
    'Kudermetova': 'RU', # Russie
    'Stakusic': 'CA',  # Canada
    'Osorio': 'CO',    # Colombie
    'Rakhimova': 'RU', # Russie
    'Sonmez': 'TR',    # Turquie
    'Maria': 'GR',     # Grèce
    'Hunter': 'US',    # États-Unis
    'Siniakova': 'CZ', # République tchèque
    'Parks': 'US',     # États-Unis
    'Vidmanova': 'CZ', # République tchèque
    'Jimenez Kasintseva': 'PE', # Pérou
    'Pridankina': 'RU', # Russie
    'Jacquemot': 'FR', # France
    'Bartunkova': 'CZ', # République tchèque
    'Herrero Linana': 'ES', # Espagne
    'Grammatikopoulou': 'GR', # Grèce
    'Tran': 'US',      # États-Unis
    'Zeballos': 'AR',  # Argentine
}

# Pays des tournois de tennis
TOURNAMENT_COUNTRIES = {
    # Tournois ATP
    'Australian Open': 'AU',
    'Roland Garros': 'FR',
    'Wimbledon': 'GB',
    'US Open': 'US',
    'Indian Wells': 'US',
    'Miami': 'US',
    'Monte Carlo': 'MC',
    'Madrid': 'ES',
    'Rome': 'IT',
    'Canada Masters': 'CA',
    'Cincinnati': 'US',
    'Shanghai': 'CN',
    'Paris Masters': 'FR',
    'ATP Finals': 'IT',
    'Hangzhou': 'CN',
    'Beijing': 'CN',
    'Tokyo': 'JP',
    'Basel': 'CH',
    'Vienna': 'AT',
    'Stockholm': 'SE',
    'Antwerp': 'BE',
    'Metz': 'FR',
    'Tel Aviv': 'IL',
    'Sofia': 'BG',
    'Rotterdam': 'NL',
    'Dubai': 'AE',
    'Acapulco': 'MX',
    'Indian Wells': 'US',
    'Barcelona': 'ES',
    'Munich': 'DE',
    'Geneva': 'CH',
    'Lyon': 'FR',
    'Stuttgart': 'DE',
    'Queens': 'GB',
    'Halle': 'DE',
    'Mallorca': 'ES',
    'Newport': 'US',
    'Hamburg': 'DE',
    'Bastad': 'SE',
    'Gstaad': 'CH',
    'Atlanta': 'US',
    'Washington': 'US',
    'Los Cabos': 'MX',
    'Winston-Salem': 'US',
    
    # Tournois WTA
    'Adelaide': 'AU',
    'Hobart': 'AU',
    'Auckland': 'NZ',
    'Shenzhen': 'CN',
    'Brisbane': 'AU',
    'Sydney': 'AU',
    'Doha': 'QA',
    'Dubai': 'AE',
    'Indian Wells': 'US',
    'Miami': 'US',
    'Charleston': 'US',
    'Stuttgart': 'DE',
    'Madrid': 'ES',
    'Rome': 'IT',
    'Strasbourg': 'FR',
    'Rabat': 'MA',
    'Roland Garros': 'FR',
    'Nottingham': 'GB',
    'Birmingham': 'GB',
    'Berlin': 'DE',
    'Eastbourne': 'GB',
    'Bad Homburg': 'DE',
    'Wimbledon': 'GB',
    'Lausanne': 'CH',
    'Budapest': 'HU',
    'Palermo': 'IT',
    'Prague': 'CZ',
    'Hamburg': 'DE',
    'Warsaw': 'PL',
    'Toronto': 'CA',
    'Cincinnati': 'US',
    'Montreal': 'CA',
    'Cleveland': 'US',
    'US Open': 'US',
    'Seoul': 'KR',
    'Seoul WTA': 'KR',
    'Guadalajara': 'MX',
    'Guadalajara 2 WTA': 'MX',
    'Sao Paulo': 'BR',
    'Sao Paulo WTA': 'BR',
    'Tokyo': 'JP',
    'Beijing': 'CN',
    'Wuhan': 'CN',
    'Linz': 'AT',
    'Ostrava': 'CZ',
    'Luxembourg': 'LU',
    'WTA Finals': 'MX',
}

# Codes pays vers noms complets pour l'affichage
COUNTRY_NAMES = {
    'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AG': 'Antigua and Barbuda',
    'AI': 'Anguilla', 'AL': 'Albania', 'AM': 'Armenia', 'AO': 'Angola', 'AQ': 'Antarctica',
    'AR': 'Argentina', 'AS': 'American Samoa', 'AT': 'Austria', 'AU': 'Australia', 'AW': 'Aruba',
    'AX': 'Åland Islands', 'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados',
    'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 'BH': 'Bahrain',
    'BI': 'Burundi', 'BJ': 'Benin', 'BL': 'Saint Barthélemy', 'BM': 'Bermuda', 'BN': 'Brunei',
    'BO': 'Bolivia', 'BQ': 'Caribbean Netherlands', 'BR': 'Brazil', 'BS': 'Bahamas', 'BT': 'Bhutan',
    'BV': 'Bouvet Island', 'BW': 'Botswana', 'BY': 'Belarus', 'BZ': 'Belize', 'CA': 'Canada',
    'CC': 'Cocos Islands', 'CD': 'DR Congo', 'CF': 'Central African Republic', 'CG': 'Republic of the Congo',
    'CH': 'Switzerland', 'CI': 'Côte d\'Ivoire', 'CK': 'Cook Islands', 'CL': 'Chile', 'CM': 'Cameroon',
    'CN': 'China', 'CO': 'Colombia', 'CR': 'Costa Rica', 'CU': 'Cuba', 'CV': 'Cape Verde',
    'CW': 'Curaçao', 'CX': 'Christmas Island', 'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DE': 'Germany',
    'DJ': 'Djibouti', 'DK': 'Denmark', 'DM': 'Dominica', 'DO': 'Dominican Republic', 'DZ': 'Algeria',
    'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'EH': 'Western Sahara', 'ER': 'Eritrea',
    'ES': 'Spain', 'ET': 'Ethiopia', 'FI': 'Finland', 'FJ': 'Fiji', 'FK': 'Falkland Islands',
    'FM': 'Micronesia', 'FO': 'Faroe Islands', 'FR': 'France', 'GA': 'Gabon', 'GB': 'United Kingdom',
    'GD': 'Grenada', 'GE': 'Georgia', 'GF': 'French Guiana', 'GG': 'Guernsey', 'GH': 'Ghana',
    'GI': 'Gibraltar', 'GL': 'Greenland', 'GM': 'Gambia', 'GN': 'Guinea', 'GP': 'Guadeloupe',
    'GQ': 'Equatorial Guinea', 'GR': 'Greece', 'GS': 'South Georgia', 'GT': 'Guatemala', 'GU': 'Guam',
    'GW': 'Guinea-Bissau', 'GY': 'Guyana', 'HK': 'Hong Kong', 'HM': 'Heard Island', 'HN': 'Honduras',
    'HR': 'Croatia', 'HT': 'Haiti', 'HU': 'Hungary', 'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel',
    'IM': 'Isle of Man', 'IN': 'India', 'IO': 'British Indian Ocean Territory', 'IQ': 'Iraq', 'IR': 'Iran',
    'IS': 'Iceland', 'IT': 'Italy', 'JE': 'Jersey', 'JM': 'Jamaica', 'JO': 'Jordan', 'JP': 'Japan',
    'KE': 'Kenya', 'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KI': 'Kiribati', 'KM': 'Comoros', 'KN': 'Saint Kitts and Nevis',
    'KP': 'North Korea', 'KR': 'South Korea', 'KW': 'Kuwait', 'KY': 'Cayman Islands', 'KZ': 'Kazakhstan',
    'LA': 'Laos', 'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LI': 'Liechtenstein', 'LK': 'Sri Lanka',
    'LR': 'Liberia', 'LS': 'Lesotho', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia',
    'LY': 'Libya', 'MA': 'Morocco', 'MC': 'Monaco', 'MD': 'Moldova', 'ME': 'Montenegro', 'MF': 'Saint Martin',
    'MG': 'Madagascar', 'MH': 'Marshall Islands', 'MK': 'North Macedonia', 'ML': 'Mali', 'MM': 'Myanmar',
    'MN': 'Mongolia', 'MO': 'Macao', 'MP': 'Northern Mariana Islands', 'MQ': 'Martinique', 'MR': 'Mauritania',
    'MS': 'Montserrat', 'MT': 'Malta', 'MU': 'Mauritius', 'MV': 'Maldives', 'MW': 'Malawi', 'MX': 'Mexico',
    'MY': 'Malaysia', 'MZ': 'Mozambique', 'NA': 'Namibia', 'NC': 'New Caledonia', 'NE': 'Niger',
    'NF': 'Norfolk Island', 'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway',
    'NP': 'Nepal', 'NR': 'Nauru', 'NU': 'Niue', 'NZ': 'New Zealand', 'OM': 'Oman', 'PA': 'Panama',
    'PE': 'Peru', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea', 'PH': 'Philippines', 'PK': 'Pakistan',
    'PL': 'Poland', 'PM': 'Saint Pierre and Miquelon', 'PN': 'Pitcairn Islands', 'PR': 'Puerto Rico',
    'PS': 'Palestine', 'PT': 'Portugal', 'PW': 'Palau', 'PY': 'Paraguay', 'QA': 'Qatar', 'RE': 'Réunion',
    'RO': 'Romania', 'RS': 'Serbia', 'RU': 'Russia', 'RW': 'Rwanda', 'SA': 'Saudi Arabia', 'SB': 'Solomon Islands',
    'SC': 'Seychelles', 'SD': 'Sudan', 'SE': 'Sweden', 'SG': 'Singapore', 'SH': 'Saint Helena',
    'SI': 'Slovenia', 'SJ': 'Svalbard and Jan Mayen', 'SK': 'Slovakia', 'SL': 'Sierra Leone', 'SM': 'San Marino',
    'SN': 'Senegal', 'SO': 'Somalia', 'SR': 'Suriname', 'SS': 'South Sudan', 'ST': 'São Tomé and Príncipe',
    'SV': 'El Salvador', 'SX': 'Sint Maarten', 'SY': 'Syria', 'SZ': 'Eswatini', 'TC': 'Turks and Caicos Islands',
    'TD': 'Chad', 'TF': 'French Southern Territories', 'TG': 'Togo', 'TH': 'Thailand', 'TJ': 'Tajikistan',
    'TK': 'Tokelau', 'TL': 'East Timor', 'TM': 'Turkmenistan', 'TN': 'Tunisia', 'TO': 'Tonga',
    'TR': 'Turkey', 'TT': 'Trinidad and Tobago', 'TV': 'Tuvalu', 'TW': 'Taiwan', 'TZ': 'Tanzania',
    'UA': 'Ukraine', 'UG': 'Uganda', 'UM': 'US Minor Outlying Islands', 'US': 'United States', 'UY': 'Uruguay',
    'UZ': 'Uzbekistan', 'VA': 'Vatican City', 'VC': 'Saint Vincent and the Grenadines', 'VE': 'Venezuela',
    'VG': 'British Virgin Islands', 'VI': 'US Virgin Islands', 'VN': 'Vietnam', 'VU': 'Vanuatu',
    'WF': 'Wallis and Futuna', 'WS': 'Samoa', 'YE': 'Yemen', 'YT': 'Mayotte', 'ZA': 'South Africa',
    'ZM': 'Zambia', 'ZW': 'Zimbabwe'
}

def get_player_nationality(player_name):
    """Obtient la nationalité d'un joueur"""
    # Nettoyer le nom du joueur
    clean_name = player_name.strip()
    
    # Chercher par nom exact d'abord
    if clean_name in PLAYER_NATIONALITIES:
        return PLAYER_NATIONALITIES[clean_name]
    
    # Chercher par nom de famille (dernier mot)
    last_name = clean_name.split()[-1] if ' ' in clean_name else clean_name
    if last_name in PLAYER_NATIONALITIES:
        return PLAYER_NATIONALITIES[last_name]
    
    # Chercher par correspondance partielle
    for known_player, nationality in PLAYER_NATIONALITIES.items():
        if known_player.lower() in clean_name.lower() or clean_name.lower() in known_player.lower():
            return nationality
    
    return None  # Nationalité inconnue

def get_tournament_country(tournament_name):
    """Obtient le pays d'un tournoi"""
    # Nettoyer le nom du tournoi
    clean_tournament = tournament_name.strip()
    
    # Chercher par nom exact
    if clean_tournament in TOURNAMENT_COUNTRIES:
        return TOURNAMENT_COUNTRIES[clean_tournament]
    
    # Chercher par correspondance partielle
    for known_tournament, country in TOURNAMENT_COUNTRIES.items():
        if known_tournament.lower() in clean_tournament.lower():
            return country
    
    return None  # Pays inconnu

def is_home_advantage(player_name, tournament_name):
    """Détermine si un joueur a l'avantage de jouer à domicile"""
    player_country = get_player_nationality(player_name)
    tournament_country = get_tournament_country(tournament_name)
    
    if player_country and tournament_country:
        return player_country == tournament_country
    
    return False

def get_country_flag_emoji(country_code):
    """Convertit un code pays en emoji drapeau"""
    if not country_code or len(country_code) != 2:
        return ''
    
    # Convertir le code pays en emoji drapeau Unicode
    flag_emoji = ''.join(chr(ord(c) + 127397) for c in country_code.upper())
    return flag_emoji

def get_country_name(country_code):
    """Obtient le nom complet d'un pays à partir de son code"""
    return COUNTRY_NAMES.get(country_code, country_code)

# Test des fonctions
if __name__ == "__main__":
    # Tests
    print("=== TESTS NATIONALITES ===")
    test_players = ['Djokovic', 'Swiatek', 'Alcaraz', 'Gauff', 'Unknown Player']
    for player in test_players:
        nationality = get_player_nationality(player)
        print(f"{player}: {nationality}")
    
    print("\n=== TESTS TOURNOIS ===")
    test_tournaments = ['US Open', 'Roland Garros', 'Seoul WTA', 'Hangzhou', 'Unknown Tournament']
    for tournament in test_tournaments:
        country = get_tournament_country(tournament)
        print(f"{tournament}: {country}")
    
    print("\n=== TESTS AVANTAGE DOMICILE ===")
    test_cases = [
        ('Alcaraz', 'Madrid'),
        ('Gauff', 'US Open'),
        ('Swiatek', 'Roland Garros'),
        ('Djokovic', 'Wimbledon')
    ]
    for player, tournament in test_cases:
        home_advantage = is_home_advantage(player, tournament)
        print(f"{player} a {tournament}: {'Domicile' if home_advantage else 'Exterieur'}")
