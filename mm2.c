#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

void printm(double **m, double *f,int n)
{
	for (int i = 0; i < n; i++)
	{
		for (int j = 0; j < n; j++)
		{
			printf("%f\t", m[i][j]);
			if (j == n - 1)
			{
				printf("\t%f\n", f[i]);
			}
		}
	}
	printf("\n");
}

double *gauss(double **m, double *f, int n)
{
	for (int globRowIdx = 0; globRowIdx < n; globRowIdx++)
	{
		// ведущий элемент для главной обрабатываемой строки должен быть равен 1
		double leadDevisor = m[globRowIdx][globRowIdx];
		for (int j = globRowIdx; j < n; j++)
		{
			m[globRowIdx][j] = m[globRowIdx][j] / leadDevisor;	
		}
		f[globRowIdx] = f[globRowIdx] / leadDevisor;

		for (int locRowIdx = globRowIdx + 1; locRowIdx < n; locRowIdx++)
		{
			double leadMultiplier = m[locRowIdx][globRowIdx];
			for (int j = globRowIdx; j < n; j++)
			{
				m[locRowIdx][j] -= leadMultiplier * m[globRowIdx][j];
			}
			f[locRowIdx] -= leadMultiplier * f[globRowIdx]; 
		}

		if (globRowIdx == 1)
		{
			//break;
		}
	}

	printm(m, f, n);

	double *x = calloc(n, sizeof(double));

	x[n - 1] = f[n - 1];

	for (int xIdx = n - 2; xIdx >= 0; xIdx--)
	{
		double sum = 0;
		for (int i = xIdx + 0; i < n; xIdx++)
		{
			//sum += x[i] * m[xIdx][i];
		}
		x[xIdx] = f[xIdx] - sum;
	}



	for (int i = 0; i < n; i++)
	{
		printf("%f ", x[i]);
	}
	printf("\n");

	return x;

	/*for globalProcessingRowIdx in range(m):
	leadDevisor = T[globalProcessingRowIdx][globalProcessingRowIdx]
	for processingColumnIdx in range(globalProcessingRowIdx, n):
		T[globalProcessingRowIdx][processingColumnIdx] = T[globalProcessingRowIdx][processingColumnIdx] / leadDevisor				# bring leading element to 1

	for localProcessingRowIdx in range(globalProcessingRowIdx + 1, m):
		leadMultiplier = T[localProcessingRowIdx][globalProcessingRowIdx]
		for j in range(globalProcessingRowIdx, n):
			T[localProcessingRowIdx][j] -= leadMultiplier * T[globalProcessingRowIdx][j]

	if globalProcessingRowIdx == 1:
		break*/
}

int main(int argc, char **argv)
{
	int n = 4;								// количество узлов

	double segmentSize = 11.0;				// длина рассматриваемого интервала

	double l = segmentSize / (n - 1);		// длина конечного элемента

	printf("l = %f\n", l);

											// коэффициенты уравнения конечного элемента, когда известны первые производные на концах элемента


	double a11;
	double a12;
	double a21;
	double a22;
	double b1;
	double b2;


	int form = 1; 							// 3 — кубическая функция формы, 1 — линейная функция формы
	if (form == 1)
	{
		a11 = (5*l*l + 1) / l;
		a12 = (5*l*l - 2) / (2*l);
		a21 = (5*l*l - 2) / (2*l);
		a22 = (5*l*l + 1) / l;
		b1 = 2*l;
		b2 = 2*l;
	}

	if (form == 3)
	{
		double v1 = (15*pow(l, 6) + 135*pow(l, 4) + 192*pow(l, 2) + 28) / (l*(15*pow(l, 4) + 52*pow(l, 2) + 28));		// переменные для удобства
		double v2 = (15*pow(l, 6) - 30*pow(l, 4) + 72*pow(l, 2) - 112) / (4*l*(15*pow(l, 4) + 52*pow(l, 2) + 28));
		double v3 = l*(pow(l, 2) + 4) / (3*pow(l, 2) + 2);
		double a11 = v1;
		double a12 = v2;
		double a21 = v2;
		double a22 = v1;
		double b1 = v3;
		double b2 = v3;
	}

	double deriv1 = 123;			// в решаемом варианте (23) это значение нам не известно
	double deriv2 = 1;
	double u0 = 10;
	double u_end = 123;				// в решаемом варианте (23) это значение нам не известно

	printf("hello %f\n", a11);

	// создание матрицы
	double **matrix = calloc(n, sizeof(double **));
	for (int idx = 0; idx < n; idx++)
	{
		matrix[idx] = calloc(n, sizeof(double));
	}

	double *f = calloc(n, sizeof(double));

	// инициализация матрицы
	for (int i = 0; i < n - 1; i++)
	{
		matrix[i][i] += a11;
		matrix[i][i+1] += a12;
		matrix[i+1][i] += a21;
		matrix[i+1][i+1] += a22;
		f[i] += b1;
		f[i+1] = b2;
	}	
	f[0] += -deriv1;
	f[n-1] += deriv2 ;

	matrix[0][0] = 22.81850649;
	matrix[0][1] = -13.89776786;
	matrix[0][2] = -8.104748376;
	matrix[0][3] = 2.277759740;
	f[0] = 0.825;

	matrix[1][0] = -13.89776786;
	matrix[1][1] = 22.81850649;
	matrix[1][2] = 2.277759740;
	matrix[1][3] = -8.104748376;
	f[1] = 0.825;

	matrix[2][0] = -8.104748376;
	matrix[2][1] = 2.277759740;
	matrix[2][2] = 7.355844156;
	matrix[2][3] = -0.4976055194;
	f[2] = 0.275;

	matrix[3][0] = 2.277759740;
	matrix[3][1] = -8.104748376;
	matrix[3][2] = -0.4976055194;
	matrix[3][3] = 7.355844156;
	f[3] = 0.275;


	printm(matrix, f, n);

	// удаляем первый столбец и строку матрицы
	/*
	for (int i = 0; i < n - 1; i++)
	{
		memmove(matrix[i], matrix[i + 1] + 1, (n - 1)*sizeof(double));
	}
	memmove(f, f + 1, (n - 1)*sizeof(double));
	*/

	//printm(matrix, f, n);

	gauss(matrix, f, n);

	printm(matrix, f, n);

	for (int i = 0; i < n; i++)
	{
		free(matrix[i]);		
	}
	free(f);
}