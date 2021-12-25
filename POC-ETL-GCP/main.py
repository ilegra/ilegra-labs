from etl import extract_spotify_data, transform, load

if __name__=='__main__':

    json_path = extract_spotify_data(spotify_secret_file_path="spotify_secret.json", bucket_name="poc_etl")
    transformation = transform(json_object_key=json_path)
    load_result = load(transformation)
    print(load_result)