import pandas as pd

# corpus_path = 'Corpus/Corpus.xlsx'
# message_path = 'Corpus/Default_Messages.xlsx'

def update_master_intent_entity_data(corpus_path):
    corpus = pd.read_excel(corpus_path, engine='openpyxl',
                            sheet_name='website_data')

    print('Started')

    data = []

    for index, row in corpus.iterrows():
        if str(row['Question']).lower() != 'nan':
            
            if str(row["Site_Area"]).lower() != 'nan':
                Site_Area = str(row["Site_Area"])

            if str(row["Functionality_Area"]).lower() != 'nan':
                Functionality_Area = str(row["Functionality_Area"])

            if '\n' in str(row["Entities"]):
                entities = str(row["Entities"]).split('\n')

                for entity in entities:
                    if str(row["Intents"]).replace("'", "''") != 'nan' and str(entity).replace("'", "''") != 'nan':
                        data.append([Site_Area, str(row["Intents"]).replace("'", "''"), str(entity).replace("'", "''")])
                    
            else:
                if str(row["Intents"]).replace("'", "''") != 'nan' and str(row["Entities"]).replace("'", "''") != 'nan':
                    data.append([Site_Area, str(row["Intents"]).replace("'", "''"), str(row["Entities"]).replace("'", "''")])
                            

    print(data)

    df = pd.DataFrame(data, columns = ['Site_Area', 'Intents', 'Entities'])

    print(df)

    with pd.ExcelWriter(corpus_path) as writer1:
        corpus.to_excel(writer1, sheet_name = 'website_data', index = False)
        df.to_excel(writer1, sheet_name = 'master_intent_entity_mapping', index = False)

    return 'Updated'


def get_data(corpus_path):
    try:
        corpus = pd.read_excel(corpus_path, engine='openpyxl',
                            sheet_name='Sheet1')
    except:
        corpus = pd.read_excel(corpus_path, engine='openpyxl',
                            sheet_name='sheet1')

    data = []

    for index, row in corpus.iterrows():

        if str(row['Sub Functional Area']).lower() != 'nan':
            
            Site_Area = 'CB'
            Functionality_Area = ''
            Entities = ''
            Intent = ''

            if str(row["Functional Area"]).lower() != 'nan':
                Functionality_Area = str(row["Functional Area"])

            if str(row["Keyword"]).lower() != 'nan':
                Entities = str(row["Keyword"]).replace("'", "''")

            if str(row["Sub Functional Area"]).lower() != 'nan':
                Entities = str(row["Sub Functional Area"]).replace("'", "''")

            data.append([Site_Area, Intent, Entities])


    df = pd.DataFrame(data, columns = ['Site_Area', 'Sub Functional Area', 'Keyword'])

    return corpus, df

