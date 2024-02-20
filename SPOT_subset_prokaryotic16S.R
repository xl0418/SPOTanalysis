# Input data
ASV=read.table("data/SPOT_combine_16S_18SwMetazoa_ASV_Jan2001_Aug2018_QC.csv",row.names=1,header=T,sep=",")
Taxa=read.table("data/SPOT_combine_16S_18SwMetazoa_taxonomy_Silva_PhytoRef_PR2_QC.csv",row.names=1,header=T,sep=",")
Meta=read.table("data/SPOT_Metadata_Seq_Envi_QC.csv",row.names=1,header=T,sep=",")
Fasta=read.table("data/SPOT_combine_16S_18SwMetazoa_ASV_dna-sequences.fasta",sep="\t")
asv.long = read.table("data/spot_asv_long.csv",sep=",",header=T)

# Subset of data for 16S only
id=grep("Prokaryotic_16S", Taxa$Sequence_Type)
ASV_16S=ASV[id,]
Taxa_16S=Taxa[id,]
fasta.id=which(Fasta$V1 %in% paste(">",rownames(ASV_16S),sep=""))
Fasta_16S=data.frame(Fasta$V1[sort(c(fasta.id,fasta.id+1))])

# Output data
write.table(ASV_16S,file="data/SPOT_Prokaryotic16S_ASV_Table.csv",sep=",",quote=F)
write.table(Taxa_16S,file="data/SPOT_Prokaryotic16S_Taxanomy.csv",sep=",",quote=F)
write.table(Fasta_16S,file="data/SPOT_Prokaryotic16S_ASV_dna-sequences.fasta",sep="\t",
                        row.names=F,col.names=F,quote=F)

