import pickle
import pandas as pd
import numpy as np
import re
from unidecode import unidecode

class MobilityCars():
    
    def __init__(self):
        home_path = ''
        self.sc_km_media_ano        = pickle.load(open(home_path + 'parameters/sc_km_media_ano.pkl','rb'))
        self.rs_ano_de_fabricacao   = pickle.load(open(home_path + 'parameters/rs_ano_de_fabricacao.pkl','rb'))
        self.rs_ano_modelo          = pickle.load(open(home_path + 'parameters/rs_ano_modelo.pkl','rb'))
        self.rs_odometro            = pickle.load(open(home_path + 'parameters/rs_odometro.pkl','rb'))
        self.oe_tipo_anuncio        = pickle.load(open(home_path + 'parameters/oe_tipo_anuncio.pkl', 'rb'))
        self.te_tipo                = pickle.load(open(home_path + 'parameters/te_tipo.pkl','rb'))
        self.te_cor                 = pickle.load(open(home_path + 'parameters/te_cor.pkl','rb'))
        self.te_localidade_vendedor = pickle.load(open(home_path + 'parameters/te_localidade_vendedor.pkl','rb'))
        self.te_valvulas            = pickle.load(open(home_path + 'parameters/te_valvulas.pkl','rb'))
        self.te_combustivel         = pickle.load(open(home_path + 'parameters/te_combustivel.pkl','rb'))
        self.te_veiculo             = pickle.load(open(home_path + 'parameters/te_veiculo.pkl','rb'))
        self.fe_marca               = pickle.load(open(home_path + 'parameters/fe_marca.pkl', 'rb'))
        self.fe_modelo              = pickle.load(open(home_path + 'parameters/fe_modelo.pkl', 'rb'))
        self.fe_versao              = pickle.load(open(home_path + 'parameters/fe_versao.pkl', 'rb'))
        self.fe_cilindradas         = pickle.load(open(home_path + 'parameters/fe_cilindradas.pkl', 'rb'))
        
    def data_cleaning(self, df):
        
        # removendo colunas que possuem NA's + id
        ## Filtering Data
        cols_drop = [
         'id',
         'num_fotos',
         'attr_veiculo_aceita_troca',
         'attr_veiculo_unico_dono',
         'attr_veiculo_todas_as_revisoes_feitas_pela_concessionaria',
         'attr_veiculo_ipva_pago',
         'attr_veiculo_licenciado',
         'attr_veiculo_garantia_de_fabrica',
         'attr_veiculo_todas_as_revisoes_feitas_pela_agenda_do_carro',
         'attr_veiculo_alienado']

        df = df.drop(columns=cols_drop)
        
        return df
    
    def feature_engineering(self, df4):

        def extract_power(re_string):
            hp = 'sem informação'
            if re_string is None:
                pass
            else:
                hp = re_string.group(0)
            return hp

        ## Feature Engineering
        # extraindo as cilindradas da coluna versão
        df4['cilindradas'] = df4['versao'].apply(lambda x: extract_power(re.search(r"\d+\.\d+",x)))

        # extraindo válvulas da coluna versão
        df4['valvulas'] = df4['versao'].apply(lambda x: extract_power(re.search(r"\d+V",x)))

        # extraindo combustível da coluna versão
        df4['combustivel'] = df4['versao'].apply(lambda x: 'GASOLINA' if 'GASOLINA' in x else 
                                                           'FLEX' if 'FLEX'     in x else 
                                                           'DIESEL' if 'DIESEL'   in x else 
                                                           'ÁLCOOL' if 'ÁLCOOL' in x else
                                                           'HÍBRIDO' if 'HYBRID' in x else
                                                           'HÍBRIDO' if 'HÍBRIDO' in x else 'sem informação')

        # removendo features derivadas da coluna original
        df4['versao'] = df4.apply(lambda x: x['versao'].replace(x['cilindradas'],'').replace(x['valvulas'], '').replace(x['combustivel'],'').replace(' AUTOMÁTICO', '').replace(' MANUAL', '').replace('  ',' '), axis=1)

        # retirando acentos, substituindo letras maiúsculas e espaços
        df4['cidade_vendedor'] = df4['cidade_vendedor'].apply(lambda x: unidecode(x).lower().replace(' ','_'))

        # extraindo estado
        df4['estado_vendedor'] = df4['estado_vendedor'].apply(lambda x: re.search(r'\((.*?)\)',x).group(1))

        # criando feature de localidade
        df4['localidade_vendedor'] = df4['cidade_vendedor'] + "_" + df4['estado_vendedor']

        # criando feature de km médio rodado por ano
        df4['km_media_ano_em_1k_km'] = df4['odometro']/np.round(2023 - df4['ano_modelo'] + 0.51,0)
        # arredondando e escalando por 1000 km
        df4['km_media_ano_em_1k_km'] = round(df4['km_media_ano_em_1k_km'] / 1000, 0).astype(int)

        # criando feature de agregação do veículo com marca, modelo, km_media e localidade
        df4['veiculo'] = df4['marca'].astype(str) + "_" + df4['modelo'].astype(str) + "_" + df4['km_media_ano_em_1k_km'].astype(str)
        
        return df4

    
    def data_preparation_model(self, df_prep):
        
        ## Standarization
        df_prep['km_media_ano_em_1k_km'] = self.sc_km_media_ano.transform(df_prep[['km_media_ano_em_1k_km']])


        # 6.4  Rescaling
        # 6.4.1  Robust Scaler

        df_prep['ano_de_fabricacao'] = self.rs_ano_de_fabricacao.transform(df_prep[['ano_de_fabricacao']])
        df_prep['ano_modelo'] = self.rs_ano_modelo.transform(df_prep[['ano_modelo']])
        df_prep['odometro'] = self.rs_odometro.transform(df_prep[['odometro']])

        # 6.5  Encodings
        # 6.5.1  One Hot Encode
        # blindado
        df_prep['blindado'] = df_prep['blindado'].replace({'S':1, 'N':0})

        # tipo_vendedor
        df_prep['tipo_vendedor'] = df_prep['tipo_vendedor'].replace({'PJ':1, 'PF':0})

        # tipo_anuncio
        cols_dummies = self.oe_tipo_anuncio.transform(df_prep['tipo_anuncio'].values.reshape(-1,1))
        df_prep[self.oe_tipo_anuncio.categories_[0]] = cols_dummies

        df_prep['cambio'] = df_prep['cambio'].map({'Manual':0,
                                                    'Automática Sequencial':1, 
                                                    'Semi-automática':2,
                                                    'CVT':3,
                                                    'Automatizada':4,
                                                    'Automática':4,
                                                    'Automatizada DCT':5
                                                    })

        df_prep['num_portas'] = df_prep['num_portas'].apply(lambda x: 1 if x > 2 else 0)

        # 6.5.2  Target Enconde
        # ['tipo','cor', 'localidade_vendedor','valvulas','combustivel', 'veiculo']:

        df_prep = self.te_tipo.transform(df_prep)
        df_prep = self.te_cor.transform(df_prep)
        df_prep = self.te_localidade_vendedor.transform(df_prep)
        df_prep = self.te_valvulas.transform(df_prep)
        df_prep = self.te_combustivel.transform(df_prep)
        df_prep = self.te_veiculo.transform(df_prep)


        # 6.5.3  Frequency Encode
        # 'marca', 'modelo','versao','cilindradas'

        df_prep = self.fe_marca.transform(df_prep)
        df_prep = self.fe_modelo.transform(df_prep)
        df_prep = self.fe_versao.transform(df_prep)        
        df_prep = self.fe_cilindradas.transform(df_prep)
        
        features_selected = [
        'veiculo',
        'marca',
        'km_media_ano_em_1k_km',
        'modelo',
        'versao',
        'ano_de_fabricacao',
        'ano_modelo',
        'odometro',
        'cambio',
        'tipo',
        'cilindradas',
        'combustivel',
        'localidade_vendedor'
        ]
        
        return df_prep[features_selected]
    
    
    def get_prediction(self, model, original_data, test_data):
        
        pred = model.predict(test_data)
        
        original_data['prediction'] = np.expm1(pred)
        
        return original_data.to_json(orient='records')