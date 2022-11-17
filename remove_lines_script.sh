COUNTER=0 
for file in UAVs_100/*
do  
    echo $COUNTER
    sed '501,$d' $file >> uav_$COUNTER.csv 
    ((COUNTER=COUNTER+1))
done
