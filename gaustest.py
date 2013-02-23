def printMatrix(T):
	for row in T:
		print row
	print " "

T = [[22.81850649, -13.89776786, -8.104748376, 2.277759740, 0.825],
	 [-13.89776786, 22.81850649, 2.277759740, -8.104748376, 0.825],
	 [-8.104748376, 2.277759740, 7.355844156, -0.4976055194, 0.275],
	 [2.277759740, -8.104748376, -0.4976055194, 7.355844156, 0.275]]

#T = [[2.,2.,3., 10.], [3,4.,5., 15.], [6.,7.,8., 7.]]

m = len(T)
n = len(T[0])

printMatrix(T)


for globalProcessingRowIdx in range(m):
	leadDevisor = T[globalProcessingRowIdx][globalProcessingRowIdx]
	for processingColumnIdx in range(globalProcessingRowIdx, n):
		T[globalProcessingRowIdx][processingColumnIdx] = T[globalProcessingRowIdx][processingColumnIdx] / leadDevisor				# bring leading element to 1

	for localProcessingRowIdx in range(globalProcessingRowIdx + 1, m):
		leadMultiplier = T[localProcessingRowIdx][globalProcessingRowIdx]
		for j in range(globalProcessingRowIdx, n):
			T[localProcessingRowIdx][j] -= leadMultiplier * T[globalProcessingRowIdx][j]

	if globalProcessingRowIdx == 1:
		break

printMatrix(T)




