LOAD DATA LOCAL INFILE  
'/path/to/result.csv'
INTO TABLE AllCars  
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ID,Car,Company,Engine,HorsePower,FullLength,Width,Height,Wheelbase,Price,Sales,Cluster,SalesGroup);