#!/bin/bash
echo "---------------------------------"
echo "  Hello, Volumes Reset Script!"
echo "---------------------------------"
rm -rf ./volumes/postgres_data
rm -rf ./volumes/pgadmin4_data
rm -rf ./volumes/setting
echo "-------- volumes removed --------"
mkdir -p ./volumes/postgres_data
mkdir ./volumes/pgadmin4_data
mkdir ./volumes/setting
cp ./setting/.env.* ./volumes/setting/
echo "-------- volumes created --------"