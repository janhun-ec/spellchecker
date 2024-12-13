#!/bin/bash
mkdir -p dicts
cd dicts

# for libreoffice
langs=('en' 'hu' 'ro' 'ko' 'de' 'fr' 'pl' 'pt' 'es' 'it' 'ru' 'sl' 'tr' 'sk' 'cs' 'ar')
languages=('en' 'hu_HU' 'ro' 'ko_KR' 'de' 'fr_FR' 'pl_PL' 'pt_PT' 'es' 'it_IT' 'ru_RU' 'sl_SI' 'tr_TR' 'sk_SK' 'cs_CZ' 'ar')
languagesLong=('en_US' 'hu_HU' 'ro_RO' 'ko_KR' 'de_DE_frami' 'fr' 'pl_PL' 'pt_PT' 'es_ES' 'it_IT' 'ru_RU' 'sl_SI' 'tr_TR' 'sk_SK' 'cs_CZ' 'ar')
# XXX ZH

extensions=('dic' 'aff')

# download each .dic and .aff file for each language
for i in "${!languages[@]}"; do
    echo curling "${languages[i]}" "${languagesLong[i]}"
    for extension in "${extensions[@]}"; do
        curl -o "${langs[i]}"."$extension" "https://raw.githubusercontent.com/LibreOffice/dictionaries/refs/heads/master/${languages[i]}/${languagesLong[i]}.$extension"
    done
done