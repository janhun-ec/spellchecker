#!/bin/bash
mkdir -p dicts
cd dicts

# for libreoffice
lang_codes=('en' 'hu' 'ro' 'ko' 'de' 'fr' 'pl' 'pt' 'es' 'it' 'ru' 'sl' 'tr' 'sk' 'cs' 'ar')
lang_dirs=('en' 'hu_HU' 'ro' 'ko_KR' 'de' 'fr_FR' 'pl_PL' 'pt_PT' 'es' 'it_IT' 'ru_RU' 'sl_SI' 'tr_TR' 'sk_SK' 'cs_CZ' 'ar')
lang_files=('en_US' 'hu_HU' 'ro_RO' 'ko_KR' 'de_DE_frami' 'fr' 'pl_PL' 'pt_PT' 'es_ES' 'it_IT' 'ru_RU' 'sl_SI' 'tr_TR' 'sk_SK' 'cs_CZ' 'ar')
# XXX ZH

extensions=('dic' 'aff')

# download each .dic and .aff file for each language
for i in "${!lang_codes[@]}"; do
    echo curling "${lang_codes[i]}"
    for extension in "${extensions[@]}"; do
        outputfile="${lang_codes[i]}.${extension}"
        url="https://raw.githubusercontent.com/LibreOffice/dictionaries/refs/heads/master/${lang_dirs[i]}/${lang_files[i]}.$extension"
        curl -o "$outputfile" "$url"
    done
done