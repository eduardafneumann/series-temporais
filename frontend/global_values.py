uf_codes = {
    "RO": 11,
    "AC": 12,
    "AM": 13,
    "RR": 14,
    "PA": 15,
    "AP": 16,
    "TO": 17,
    "MA": 21,
    "PI": 22,
    "CE": 23,
    "RN": 24,
    "PB": 25,
    "PE": 26,
    "AL": 27,
    "SE": 28,
    "BA": 29,
    "MG": 31,
    "ES": 32,
    "RJ": 33,
    "SP": 35,
    "PR": 41,
    "SC": 42,
    "RS": 43,
    "MS": 50,
    "MT": 51,
    "GO": 52,
    "DF": 53
}

skin_color_codes = {
    "Ign/Branco": 0,
    "Branca": 1,
    "Preta": 2,
    "Amarela": 3,
    "Parda": 4,
    "Indigena": 5
}

sex_codes = {
    "Ignorado": 0,
    "Masculino": 1,
    "Feminino": 2
}

inverted_uf_codes = {v: k for k, v in uf_codes.items()}
inverted_skin_color_codes = {v: k for k, v in skin_color_codes.items()}
inverted_sex_codes = {v: k for k, v in sex_codes.items()}