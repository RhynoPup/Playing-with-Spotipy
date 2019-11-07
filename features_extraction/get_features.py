import pprint,json,os,time,glob

def get_playlist_names(sp,username):
    data =[]
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        data.append(playlist)
        #playlist_names.append(playlist['name'])
    return data

def show_tracks(tracks,tracklist):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        tracklist.append(track)
    return tracklist


def get_playlist_tracks(sp,username,user_playlists_file):
    os.makedirs('data',exist_ok=True)
    data = json.loads(open(user_playlists_file,'r').read())
    for playlist_ind, playlist in enumerate(data):
        if (playlist_ind>-1):

            playlist_id =playlist['name']
            playlist_owner = playlist['owner']['id']
            savename ='data/playlist_tracks_'+str(playlist_owner)+"_"+str(playlist_id.replace(' ','_').replace(')','').replace('(','').replace(',','').replace('?','').replace('/',''))+'.json'

            if not os.path.exists(savename):
                print(playlist_owner)
                master_list =[]
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(playlist_owner, playlist['id'],
                                           fields="tracks,next")
                tracks = results['tracks']
                master_list = show_tracks(tracks,master_list)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    master_list = show_tracks(tracks,master_list)
                with open(savename,'w') as f:
                    f.write(json.dumps(master_list))
                f.close()
                time.sleep(.5)

def compile_tracks(sp,filestart,trackrepo):
    playlists = glob.glob(os.path.join('..','data',filestart+"*.json"))

    if not os.path.exists(trackrepo):
        repo = dict()
        with open(trackrepo,'w') as f:
            f.write(json.dumps(repo))
        f.close()

    for ind,playlist in enumerate(playlists):
        with open(trackrepo, 'r') as trackrepo_file:
            repo = json.loads(trackrepo_file.read())
        trackrepo_file.close()
        #temp = dict()
        if ind>-1:
            print(playlist)
            with open(playlist,'r') as f:
                data = json.loads(f.read())
                #print('there are ', len(data), ' tracks in this playlist')

                for track_ind, track in enumerate(data):
                    if track_ind>-1:
                        if data[track_ind]['id'] not in repo.keys():
                            try:
                                repo[data[track_ind]['id']]=sp.audio_features(data[track_ind]['id'])
                            except:
                                print(data[track_ind]['name'],data[track_ind]['id'])
                                continue
                            #temp[data[track_ind]['id']]=sp.audio_features(data[track_ind]['id'])

                #pprint.pprint(len(repo))
        with open(trackrepo, 'w') as trackrepo_file:
            trackrepo_file.write(json.dumps(repo))
        trackrepo_file.close()

def check_attr_existence(attr_name,output,output_track, track_iter):
    pprint.pprint(attr_name in output[output_track].keys())
    if attr_name in track_iter.keys():
        #print(attr_name, track_iter[attr_name], type(track_iter[attr_name]))
        if type(track_iter[attr_name])!=list:
            attribute = [str(track_iter[attr_name])]
            print(attr_name,attribute, type(attribute),attr_name in output[output_track].keys())
            if attr_name in output[output_track].keys():
                print(output[output_track][attr_name])
                if  ([output[output_track][attr_name]]!=attribute):
                    if (type(output[output_track][attr_name])!=list):
                        output[output_track][attr_name] =[output[output_track][attr_name]]
                        output[output_track][attr_name].extend(attribute)
                    else:
                        output[output_track][attr_name].extend(attribute)

            else:
                if type(attribute) != list:
                    output[output_track][attr_name] = [str(attribute)]
                else:
                    output[output_track][attr_name] = attribute
        else:
            attribute = track_iter[attr_name]
            if attr_name in output[output_track].keys():
                output[output_track][attr_name].extend(attribute)
            else:
                output[output_track][attr_name] = attribute
    else:
        attribute = []


    return output

def build_spreadsheet():
    playlist_names_base = 'playlists_'
    playlist_tracks_base = 'playlist_tracks'
    track_repo = 'track_repo.json'
    data_dir = 'data'
    output = dict()
    repo = json.loads(open(os.path.join(data_dir,track_repo),'r').read())

    for track_ind, track in enumerate(repo):
        if track_ind>-1:
            #print(track)
            if track_ind%10==0:
                print(track_ind)
            output[track] =repo[track][0]
            for playlist_ind,playlist in enumerate(glob.glob(os.path.join(data_dir,playlist_tracks_base+'*.json'))):
                if playlist_ind>-1:
                    matching_tracks = [item for item in json.loads(open(playlist,'r').read()) if track==item['id']]
                    if matching_tracks:
                        for track_iter in matching_tracks:
                            #print(track_iter['name'])

                            #pprint.pprint(track_iter)
                            output[track]['name']=track_iter['name']
                            output[track]['popularity']=track_iter['popularity']

                            #----- ARTISTS ----------------------
                            track_artists = track_iter['artists']

                            if 'artists' in output[track].keys():
                                artists = output[track]['artists']
                                [artists.append(item) for item in track_artists if
                                 item['id'] not in [art_item['id'] for art_item in artists]]
                            else:
                                output[track]['artists'] = []
                                artists = output[track]['artists']
                                [artists.append(item) for item in track_artists]

                            # ----- ALBUMS ----------------------
                            if 'album' in track_iter.keys():
                                track_album = track_iter['album']
                            else:
                                track_album = []

                            if 'album' in output[track].keys():
                                if type(output[track]['album'])==dict:
                                    if (track_album['id'] not in output[track]['album']['id'] ):
                                        output[track]['album'] =[output[track]['album']]
                                        output[track]['album'].append(track_album)
                                else:
                                    if (track_album['id'] not in [item['id'] for item in output[track]['album']]):
                                        output[track]['album'].append(track_album)
                            else:
                                output[track]['album'] = track_album

                            # ----- MARKETS ----------------------
                            if 'available_markets' in track_iter.keys():
                                available_markets = track_iter['available_markets']
                            else:
                                available_markets = []

                            if 'available_markets' in output[track].keys():
                                output[track]['available_markets'].extend(available_markets)
                            else:
                                output[track]['available_markets'] = available_markets

                    #output[track]['artists']= artists
            #pprint.pprint(track)
    with open('data/attribute_repo.json','w') as f:
        f.write(json.dumps(output))
    f.close()