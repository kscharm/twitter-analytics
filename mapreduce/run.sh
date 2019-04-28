while :
do
    python3 download.py
    hdfs dfs -rmr /user/raw.txt
    hdfs dfs -put /home/sshuser/raw.txt /user/raw.txt
    hdfs dfs -rmr /user/word-count
    yarn jar /usr/hdp/2.6.5.3008-11/hadoop-mapreduce/hadoop-streaming.jar -files /home/sshuser/mapper.py,/home/sshuser/reducer.py -mapper mapper.py -reducer reducer.py -input /user/raw.txt -output /user/word-count
    rm -f word-count.txt
    hdfs dfs -get /user/word-count/part-00000 word-count.txt
    python3 upload.py
    sleep 25
done