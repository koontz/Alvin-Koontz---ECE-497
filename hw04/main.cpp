/*
Author: Alvin Koontz
Date: 9/27/2016
*/


#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>

using namespace std;

const int GRID_SIZE = 4;

class GridCharacter{
public:
	char value;	
	GridCharacter ** neighbors; 
	int numberOfneighbors;
	int x;
	int y;
	GridCharacter(char c,int x,int y);
	void addNeighbor(GridCharacter *c);
	bool containsString(string s);
private:
	bool containsString(string s, int index,GridCharacter *lastVisted);
};
GridCharacter::GridCharacter(char c,int x,int y){
	this->value = c;
	this->x = x;
	this->y = y;
	this->numberOfneighbors = 0;
	neighbors = (GridCharacter**) malloc(sizeof(GridCharacter*)*8);//8 max neighbors
//	cout<<this->x<<this->y<<' '<<this->value<<"\n";
}
void GridCharacter::addNeighbor(GridCharacter *c){
	if(abs((c->x) - (this->x))==0 && abs((c->y) - (this->y))==0){
//		cout<<c->value<<c->value<<"\n";
		return;	
	}
	if(abs((c->x) - (this->x))<2 && abs(c->y - this->y)<2){
//		cout<<this->x<<this->y<<' '<<this->value<<"  :  ";
//		cout<<c->x<<c->y<<' '<<c->value<<"\n";
		this->neighbors[numberOfneighbors] = c;
		this->numberOfneighbors+=1;
	}
}
bool  GridCharacter::containsString(string s){
	bool output = false;
	if(s[0]==this->value){
//		cout<<s<<"\n";
		for(int i = 0;i<this->numberOfneighbors;i++){
			output = output | this->neighbors[i]->containsString(s,1,this);
		}
	}
	return output;
}
bool  GridCharacter::containsString(string s, int index, GridCharacter *lastVisted){
	bool output = false;
	if(index+1 > s.length()){
		//cout<<"hit"<<index<<'\n';
		return true;
	}if(s[index]==this->value){
//		cout<<s<<index<<"\n";
		for(int i = 0;i<this->numberOfneighbors;i++){
			if(lastVisted!=this->neighbors[i]){
				output = output | this->neighbors[i]->containsString(s,index+1,this);
			}
		}
	}
	return output;
}

string lowerCase(string s){
	locale loc;
	for(int i=0;i<s.length();i++){
		s[i] =tolower(s[i],loc);
	}
	return s;
}


int main(int argc, char **argv){
	ifstream inFile;
	GridCharacter* grid[GRID_SIZE*GRID_SIZE];
	int i,j;
	string line;

//	cout <<argc <<"\n";
	if(argc<3){
		cout<<"Inccorect number of arguments: "<<argc<< ", when 3 are expected\n" <<"exiting\n";
		return 0;
	}
	string wordListFile = argv[1];
	string input = argv[2];
//	cout <<wordListFile<<"\n";
//	cout <<input<<"\n";
	inFile.open(wordListFile.c_str());


	for(i=0;i<GRID_SIZE;i++){
		for(j=0;j<GRID_SIZE;j++){
			//grid[i][j] = input[i*4+j];
			grid[i*GRID_SIZE+j] = new GridCharacter(input[i*GRID_SIZE+j],j,i);
		}
	}
	for(int k =0;k<GRID_SIZE*GRID_SIZE;k++){
		for(i=0;i<GRID_SIZE;i++){
			for(j=0;j<GRID_SIZE;j++){
				grid[k]->addNeighbor(grid[i*GRID_SIZE+j]);
			}
		}
	}

//	cout<<grid[0]->numberOfneighbors<<"\n";
//	cout<<grid[0]->value<<"\n";
//	cout<<grid[0]->neighbors[0]->value<<"\n";
	//printGrid(grid);
	line = "ABANDON";
//	cout<<grid[0]->containsString(lowerCase(line))<<"\n";
	//string output = "Hello World!";
	//cout << output <<endl;
	bool flag = false;
	while(getline(inFile,line)){
		for(i=0;i<GRID_SIZE*GRID_SIZE;i++){
			flag = flag | grid[i]->containsString(lowerCase(line));
		}
		if(flag){
			cout<<line<<"\n";
		}
		flag = false;
	}
	inFile.close();
	return 0;
}
