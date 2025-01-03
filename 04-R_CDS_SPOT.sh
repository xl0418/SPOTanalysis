#!/bin/bash

# Define the download function with one line from the tsv file as the feed-in
CDS_data(){
    str2="$(echo $1 | cut -d ',' -f 1)"

    opttemp="$(echo $1 | cut -d ',' -f 2)"
    
    prokkaoutput="prokkaSPOT"

    # create folders to hold annotated genomes for $str2
    gff_file="${prokkaoutput}/${str2}/${str2}.gff"
    cds_file="${str2}_CDS_names.txt"

    # generate CDS names
    sed -n '/##FASTA/q;p' $gff_file | awk '$3=="CDS"' | awk '{print $9'} | awk 'gsub(";.*","")' | awk 'gsub("ID=","")' > $prokkaoutput/$str2/$cds_file
    sleep 1
    Rscript 04-gRodonSPOTGenomes_sT.R $str2
    sleep 1
    Rscript 04-gRodonSPOTGenomes_vT.R $str2 $opttemp

}
export -f CDS_data

echo "CDS Starts"

# The second argument specifies the input file
inputfile=$2

# parallel the download function with the first argument specifying number of cores
cat $inputfile | parallel -j $1 CDS_data

echo "Done"


