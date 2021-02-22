import os
import re


def intersection(lst1, lst2): 
    """ Find intersection of two lists """
    intersect = [value for value in lst1 if value in lst2] 
    return intersect


def digits_only(text):
    """ Verify the files used are only those prefixed with digits """
    return re.match(r'^([\s\d]+)$', text)


def read_file_ids(dir_files):
    """ Extract file ids from full file names """
    return [file_id.split('_')[0] for file_id in dir_files if digits_only(file_id.split('_')[0])]


def read_lang_dirs(dir_to_read):
    """ For each language, construct a dictionary of ids in it """
    all_dirs = [lang for lang in os.walk(dir_to_read)]
    lang_dirs = [lang.split('_')[1] for lang in all_dirs[0][1]]
    file_id_dirs = {}

    for index, i in enumerate(all_dirs):
        # Run only over files
        if index > 0:
            file_id_dirs[lang_dirs[index-1]] = read_file_ids(i[2]) 
    return file_id_dirs


def compare_lang_dirs(prev_dir, cur_dir):
    """ 
      - Go in parallel over language, previous values and current values and find the unique ones 
      @params: prev_dir - dictionary where the key is a language, the value is a list of ids found,
               cur_dir - dictionary where the key is a language, the value is a list of ids found  
    """
    result = []
    for i in zip(prev_dir.items(), cur_dir.items()):
        # Each entry in our dictionary item is key and value tuple
        prev_values = i[0][1]
        cur_values = i[1][1]
        # Find the intersection and if it's not empty extend resulting list
        intersect = intersection(cur_values, prev_values)
        if len(intersect):
            result.extend(intersect)
    # Get rid of duplicates and sort out before returning
    return sorted(set(result))


def find_id_overlap(prev_dir, cur_dir):
    """ Find the id overlap of two directories """
    run_dir = os.getcwd()
    # Use the absolute path
    prev_dir = run_dir+prev_dir
    cur_dir = run_dir+cur_dir
    # Read a list of dictionaries - language and a list of ID-ed files for previous dir
    lang_dirs_prev = read_lang_dirs(prev_dir)
    # Read a list of dictionaries - language and a list of ID-ed files for current dir   
    lang_dirs_cur = read_lang_dirs(cur_dir)
    # Compare two directories and return the list of non-repeating IDs 
    nonDuplicates = compare_lang_dirs(lang_dirs_prev, lang_dirs_cur)
    # Print out result
    for dup in nonDuplicates:
        print(dup)   
 

if __name__ == '__main__':
    fst = "/test_files/FIRST"
    snd = "/test_files/SECOND"
    find_id_overlap(fst, snd)
