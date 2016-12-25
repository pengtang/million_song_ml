# Convert h5 files to mat files and last csv files
# Usage: python convert_h5_to_csv.py <h5_directory/h5_files>
import os
import sys
import scipy.io
import numpy as np
import pandas as pd
from hdf5_to_matfile import transfer, get_all_files

class Song:
	def __init__(self):
		self.artist_name = []
		self.title = []
		self.release = []
		self.track_id = []
		self.start_of_fade_out = []
		self.duration = []
		self.year = []
		self.artist_location = []
		self.labels = ["artist_name", "title", "release", "track_id", "start_of_fade_out", "duration", "year", "artist_location"]

	def make_data_frame(self):
		self.df = [self.artist_name, self.title, self.release, self.track_id, self.start_of_fade_out, self.duration, self.year, self.artist_location]
		df = pd.DataFrame(self.df).T
		#df.columns = self.labels
		return df

	def __str__(self):
		return str([self.artist_name, self.title, self.release, self.track_id, self.start_of_fade_out, self.duration, self.year, self.artist_location])

# .mat file will be generated in the same directory
if len(sys.argv) != 2:
	print "Usage: python convert_h5_to_csv.py <h5_directory/h5_files>"
	sys.exit(0)

# GET DIR/FILE
if not os.path.exists(sys.argv[1]):
    print 'file or dir:',sys.argv[1],'does not exist.'
    sys.exit(0)
if os.path.isfile(sys.argv[1]):
    if os.path.splitext(sys.argv[1])[1] != '.h5':
        print 'we expect a .h5 extension for file:',sys.argv[1]
        sys.exit(0)
    allh5files = [ os.path.abspath(sys.argv[1]) ]
elif not os.path.isdir(sys.argv[1]):
    print sys.argv[1],"is neither a file nor a directory? confused... a link? c'est klug?"
    sys.exit(0)
else:
    allh5files = get_all_files(sys.argv[1],ext='.h5')
if len(allh5files) == 0:
    print 'no .h5 file found, sorry, check directory you gave us:',sys.argv[1]

if len(allh5files) > 1000:
    print 'you are creating',len(allh5files),'new matlab files, hope you have the space and time!'

# Now transform h5 files to mat files.
transform_count = 0
count = 0
total_h5_count = len(allh5files)
indication_list = [ total_h5_count/10 * i for i in range(1,10)]
for f in allh5files:
	filedone = transfer(f)
	if filedone:
		transform_count += 1

	if total_h5_count >= 10:
		count += 1
		if count in indication_list:
			print "Now you are " + str((indication_list.index(count) + 1) * 10) + "% of transforming from h5 to mat task"

print "You successfully transformed " + str(transform_count) + " files(if mat file is already there it won't count as transformed)"

# Now we are going to transform the mat files to csv files.
if os.path.isfile(sys.argv[1]):
    allmatfiles = [ os.path.abspath(sys.argv[1])[:-3] + ".mat" ]
elif not os.path.isdir(sys.argv[1]):
    print sys.argv[1],"is neither a file nor a directory? confused... a link? c'est klug?"
    sys.exit(0)
else:
    allmatfiles = get_all_files(sys.argv[1],ext='.mat')


songs = Song()
my_df = songs.make_data_frame()
my_df.to_csv('my_csv.csv', index=False, header=songs.labels, sep = '|')

total_matfile_count = len(allmatfiles)
indication_list = [ total_matfile_count/10 * i for i in range(1,10)]
matfile_finish_count = 0
fail_count = 0
for f in allmatfiles:
	#print "The filename is: ", f
	try:
		data = scipy.io.loadmat(f)
		#print "tempo: ", data['tempo'], "energy: ", data['energy'], "song_hotness: ", data['song_hotttnesss'] , "loudness: ", \
		#	  data['loudness']
		#print "duration: ", data['duration'], " start_of_fade_out", data['start_of_fade_out']

		songs = Song()
		#		songs.artist_name.append(str(data['artist_name'].item(0))) #sometimes the value is empty, it's going to throw exception
		songs.artist_name.append(str(data['artist_name'])[3:-2])
		songs.title.append(str(data['title'])[3:-2])
		songs.release.append(str(data['release'])[3:-2])
		songs.track_id.append(str(data['track_id'])[3:-2])
		songs.start_of_fade_out.append(str(data['start_of_fade_out'])[3:-2])
		songs.duration.append(str(data['duration'])[3:-2])
		songs.year.append(str(data['year'])[2:-2])
		songs.artist_location.append(str(data['artist_location'])[3:-2])
		# print "the variable songs is: "
		# print songs
		my_df = songs.make_data_frame()
		my_df.to_csv('my_csv.csv', index=False, header= False, sep = '|', mode = 'a')

	except TypeError:
		fail_count += 1

	finally:
		# Show how much the task progresses
		if total_matfile_count >= 10:
			matfile_finish_count += 1
			if matfile_finish_count in indication_list:
				print "Now you are " + str((indication_list.index(matfile_finish_count) + 1) * 10) + "% of writing to csv task"

print "There are " + str(total_matfile_count) + " matfiles, we failed to get " + str(fail_count) + " songs info"
