BEGIN{
x = 4;
y = 11;
n=0;
xr = 0;
xp = 0;
xa;
s2;
a2;
data1[22];
data2[22];
data3[22];
total_akurasi = 0;
total_precision = 0;
total_recal = 0;
}
{
if(NR == x){
	print $2,$3
	total_precision = total_precision + $2
	xp = xp + ($2*$2)
	total_recal = total_recal + $3
	xr = xr + ($3*$3)
	x=x+11
	n++
}
if(NR == y){
	print $2
	xa = xa+($2*$2)
	#print xa
	total_akurasi = total_akurasi + $2 
	y=y+11
}

}
END{	
	print total_akurasi
	print "Mean : ",total_akurasi/n
	printf("Presentase : %f"%(total_akurasi/n/100))

	print total_recal
	print "Mean : ",total_recal/n
	printf("Presentase : %f"%(total_recal/n/100))

	print total_precision
	print "Mean : ",total_precision/n
	printf("Presentase : %f",(total_precision/n/100))

#	print "\n\n"
#	print "Median",n/2

#	X = total_akurasi
#	X2 = xa
	
#	a2 = sqrt(n*(X * X)-(X2))/(n*(n-1))
#	print a2

	#print xr
	#print total_recal

	#print xp
	#print total_precision
	
}
