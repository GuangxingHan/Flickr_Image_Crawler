import os
from multiprocessing import Pool
import requests
import urllib.request
import urllib.parse
import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fuzzywuzzy import utils
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()
import heapq
import sys
sys.path.insert(0, '../')
import flickr_api as f
import csv
import argparse

parser = argparse.ArgumentParser(description='Flickr_Image_Crawler')
parser.add_argument('--part_id', type=int, default=0, help='part_id')

args = parser.parse_args()



return_candidate = 30

stop_words = set(stopwords.words('english'))
stop_words.add("metropolitan")
stop_words.add("museum")
stop_words.add("art")
print("stop_words=", stop_words)

with open('../../../MetObjects_filter.csv') as MET_file:
    reader = csv.DictReader(MET_file, delimiter=',')

    tot_lines = 0
    # title_count = {}
    # title_id = {}
    object_id_dict_v1 = {}
    object_id_dict_v2 = {}
    for row in reader:
        tot_lines += 1
        # if row['Is Public Domain'] == 'True':
        #     continue
        # object_string = row['Title'] + ' ' + row['Artist Display Name']
        object_string_v1 = row['Title']
        object_string_v1 = utils.full_process(object_string_v1)
        if object_string_v1 != '':
            object_id_dict_v1[row['Object ID']] = object_string_v1

        object_string_v2 = row['Title'] + ' ' + row['Artist Display Name']
        object_string_v2 = utils.full_process(object_string_v2)
        if object_string_v2 != '':
            object_id_dict_v2[row['Object ID']] = object_string_v2
        # title_id[object_string] = row['Object ID']
        # if object_string in title_count:
        #     title_count[object_string] += 1
        # else:
        #     title_count[object_string] = 1

    # print('$$$$$$$$$$$$$$$$$$$$ len(title_id)=', len(title_count))
    print('$$$$$$$$$$$$$$$$$$$$ len(object_id_dict_v1)=', len(object_id_dict_v1))
    print('$$$$$$$$$$$$$$$$$$$$ len(object_id_dict_v2)=', len(object_id_dict_v2))


MET_artwork_exhibit_url = {}
with open('/home/guangxing/projects/artwork_datasets/MetObjects.csv') as MET_dataset:
    reader = csv.DictReader(MET_dataset, delimiter=',')
    for row in reader:
        MET_artwork_exhibit_url[row['Object ID']] = row['Link Resource']


MET_download_url = {}
with open('/home/guangxing/projects/artwork_datasets/MET_dataset.csv') as MET_dataset:
    reader = csv.DictReader(MET_dataset, delimiter=',')
    for row in reader:
        if row['Object ID'] in MET_download_url:
            continue
        else:
            MET_download_url[row['Object ID']] = row['URL']


def match_function(s1, s2):
    word_tokens_s1 = word_tokenize(s1)
    word_tokens_clean_s1 = [w for w in word_tokens_s1 if not w in stop_words]
    # word_tokens_clean_s1_stemmed = [porter.stem(word) for word in word_tokens_clean_s1]
    token_s1 = set(word_tokens_clean_s1)

    word_tokens_s2 = word_tokenize(s2)
    word_tokens_clean_s2 = [w for w in word_tokens_s2 if not w in stop_words]
    # word_tokens_clean_s2_stemmed = [porter.stem(word) for word in word_tokens_clean_s2]
    token_s2 = set(word_tokens_clean_s2)

    # if len(token_s2) == 0:
    #     return 0.0

    intersection = token_s1.intersection(token_s2)
    # score = len(intersection) / len(token_s2)

    union = token_s1.union(token_s2)
    if len(union) == 0:
        score = 0.0
    else:
        score = float(len(intersection)/len(union))

    # len_s1 = len(token_s1)
    # len_s2 = len(token_s2)
    # len_ratio = float(len_s1 / len_s2)
    # if len_ratio >= 8:
    #     score = score * 0.6

    # print(token_s1, token_s2, intersection)
    return score

def match_database(s1, choices, limit=return_candidate):
    s1 = utils.full_process(s1)
    candidate = []
    for key, choice in choices.items():
        score = match_function(s1, choice)
        if score >= 0:
            candidate.append((choice, score, key))
    return heapq.nlargest(limit, candidate, key=lambda i: i[1]) if limit is not None else \
        sorted(candidate, key=lambda i: i[1], reverse=True)


# s1 = "Badge of the Cincinnati Medal"
# s1 = "the flight into egypt, cosmè tura (cosimo di domenico di bonaventura) (italian, ferrara, active by 1451–died 1495 ferrara)early 1470s. met, nyc"
# s1 = "Dancing Celestial"
# s1 = "Metropolitan Museum of Art Dancing Celestial India (Uttar Pradesh), early 12th century Sandstone"
# s1 = "Celestial dancer (Devata)"

# print("before utils.full_process, s1=", s1)
# s1 = utils.full_process(s1)
# print("after utils.full_process, s1=", s1)
# word_tokens_s1 = word_tokenize(s1)
# print("after word_tokenize, s1=", word_tokens_s1)
# word_tokens_clean_s1 = [w for w in word_tokens_s1 if not w in stop_words]
# print("after remove stop_words, s1=", word_tokens_clean_s1)
# word_tokens_clean_s1_stemmed = [porter.stem(word) for word in word_tokens_clean_s1]
# print("after stemming, s1=", word_tokens_clean_s1_stemmed)

# print(match_database(s1, object_id_dict, limit=return_candidate))
# s2 = "the banquet of the Starved, Detail 4,  james ensor (belgian, ostend 1860–1949 ostend)"
# s1 = utils.full_process(s1)
# print(match_function(s1, s2))


photo_objects = []
file1 = open('peter/images_links_final_peter_part_'+str(args.part_id)+'.csv', 'w', newline='')
fieldnames = ['Query_Id', 'Query_ImageURL', 'Query_FlickrURL', 'Query_title', 'Query_Description']
for idx in range(1,21):
    fieldnames.append('Candidate_Artwork{}_Id'.format(idx))
    fieldnames.append('Candidate_Artwork{}_ImageURL'.format(idx))
    fieldnames.append('Candidate_Artwork{}_ExhibitURL'.format(idx))
writer1 = csv.DictWriter(file1, fieldnames=fieldnames)
writer1.writeheader()

def get_url(p):
    candidates = ['url_o', 'url_l', 'url_c', 'url_z', 'url_n', 'url_m', 'url_q', 'url_s', 'url_t', 'url_sq']
    for candidate in candidates:
        if candidate in p.__dict__.keys():
            url = p[candidate]
            break
    return url

# import threading
# csv_writer_lock = threading.Lock()

def write_to_csv(indice, p, MET_candidate, Query_title, Query_Description):
    base_url = 'https://www.flickr.com/photos'
    output_dict = {}
    output_dict['Query_Id'] = indice
    output_dict['Query_ImageURL'] = get_url(p)
    output_dict['Query_FlickrURL'] = base_url+'/'+p.owner.id+'/'+p.id
    output_dict['Query_title'] = Query_title
    output_dict['Query_Description'] = Query_Description
    count = 0
    for idx in range(len(MET_candidate)):
        MET_id = MET_candidate[idx]
        if MET_id in MET_download_url and MET_id in MET_artwork_exhibit_url:
            field_name1 = 'Candidate_Artwork{}_Id'.format(count+1)
            field_name2 = 'Candidate_Artwork{}_ImageURL'.format(count+1)
            field_name3 = 'Candidate_Artwork{}_ExhibitURL'.format(count+1)
            output_dict[field_name1] = MET_id
            output_dict[field_name2] = MET_download_url[MET_id]
            output_dict[field_name3] = MET_artwork_exhibit_url[MET_id]
            count += 1
            if count == 20:
                break
    # print("before writing ==================== \n{}".format(output_dict))
    # with csv_writer_lock:
    writer1.writerow(output_dict)
    file1.flush()
    # print("after writing ==================== ")


def download_images(indice):
    def remove(value, deletechars):
        for c in deletechars:
            value = value.replace(c,'')
        return value

    p = photo_objects[indice]
    # print(p.__dict__)
    title_tmp = p.title
    description_tmp = p.description

    print('################### Processing ', indice)
    print('query title:', title_tmp, '\n******\nquery description:', description_tmp)

    results1 = []
    if title_tmp != '':
        results1 = match_database(title_tmp, object_id_dict_v1, limit=return_candidate)
        results1 = sorted(results1, key=lambda student: student[1], reverse=True)


    results2 = []
    if description_tmp != '':
        results2 = match_database(description_tmp, object_id_dict_v2, limit=return_candidate)
        results2 = sorted(results2, key=lambda student: student[1], reverse=True)

    # merge_results = results1 + results2
    # merge_results = sorted(merge_results, key=lambda student: student[1], reverse=True)
    # print('merge_results:', merge_results)
    print("matching with flickr title: ", results1)
    print("matching with flickr description: ", results2)

    vis = set()
    count = 0
    MET_candidate = []
    for id_ in range(len(results1)):
        if results1[id_][2] in vis:
            continue
        MET_candidate.append(results1[id_][2])
        vis.add(results1[id_][2])
        count += 1
        if count == return_candidate-5:
            break

    for id_ in range(len(results2)):
        if results2[id_][2] in vis:
            continue
        MET_candidate.append(results2[id_][2])
        vis.add(results2[id_][2])
        count += 1
        if count == return_candidate:
            break

    write_to_csv(indice, p, MET_candidate, title_tmp, description_tmp)


def find_photo_objects_by_group():
    user_id = 'abc'
    user_ids = [user_id,]

    access_token = 'auth1.txt'
    f.set_auth_handler(access_token)

    g = f.Group.getByUrl('https://www.flickr.com/groups/metmuseum/')
    print(g.__dict__)

    for count_, id_ in enumerate(user_ids):
        ps = g.getPhotos(user_id=id_, extras='description', per_page='500')
        # print(ps.info, ps.info['total'])

        for page_photo in range(1, ps.info['pages']+1):
            # license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o
            ps = g.getPhotos(user_id=id_, extras='description, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o', per_page='500', page=str(page_photo))
            # print('page_photo: ', page_photo, ' has ', len(ps.data), ' photos')

            for p in ps.data:
                # print(p.__dict__)
                photo_objects.append(p)

        print('processing user ', count_, '. Total images: ', len(photo_objects))


def find_photo_objects_by_person():
    flickr_username = "abc"
    u = f.Person.findByUserName(flickr_username)
    # print(u.__dict__)
    count = 0
    ps_all = u.getPhotosets()
    # print(ps_all)
    print("The total number of galleries of Peter Roan=", ps_all.info['total'])
    for page_gallery in range(1, ps_all.info['pages']+1):
        ps_all = u.getPhotosets(page=str(page_gallery))
        for ps in ps_all:
            if 'Metropolitan' in ps.title:
                print("current gallery title=", ps.title)
                photos = ps.getPhotos()
                print("The number of photos in the current gallery=", photos.info['total'])
                for page_photo in range(1, photos.info['pages']+1):
                    photos = ps.getPhotos(extras='description, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o', per_page='500', page=str(page_photo))
                    for p in photos.data:
                        photo_objects.append(p)
                        count += 1


find_photo_objects_by_person()
# find_photo_objects_by_group()
print(len(photo_objects))

print("Processing part {}. From photo {} to photo {}".format(args.part_id, 1000*args.part_id, 1000*(args.part_id+1)-1))
for idx in range(1000*args.part_id, min(1000*(args.part_id+1), len(photo_objects))):
    download_images(idx)

file1.close()
