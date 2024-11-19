import api_data_manager as apm

df_sport = apm.get_sports_info(1)
print(df_sport.to_string())