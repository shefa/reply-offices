#include<bits/stdc++.h>
using namespace std;

#define ANNEALING_FEED 0
#define DEBUG_PRINT 1
#define endl '\n'
#define mp make_pair
#define pii pair<int,int>


/* Timing stuff */
double currentTime=0;
double deadline=CLOCKS_PER_SEC*4.5;
inline int getTime() { return currentTime=clock(); }

vector<string> ma3x;
int placed[1000][1000];
int global_score=0;
int m,n;

struct developer{
	int c;
	int b;
	unordered_set<int> skills;
};

vector<developer> devs;
vector<developer> managers;

vector<pii> ans;


int moves[4][2] = {{-1,0}, {1,0}, {0,-1}, {0,1}};


int score_btw2(developer &x, developer &y){
	int obshto=0;
	if(x.skills.size()&&y.skills.size()){
		for(auto &i:x.skills){
			if(y.skills.find(i)!=y.skills.end()) obshto++;
		}
		obshto*=(x.skills.size()+y.skills.size()-2*obshto);
	}
	return obshto+(x.c==y.c?x.b*y.b:0);
}


void filter_map(){
	for(int i=0;i<n;i++){
		for(int j=0;j<m;j++){
			if(ma3x[i][j]=='#') continue;
			bool found=0;
			for(int z=0;z<4;z++){
				int x=i+moves[z][0];
				int y=j+moves[z][1];
				if(x>=0&&x<n&&y>=0&&y<m&&ma3x[x][y]!='#') found=1;
			}
			if(found==0) ma3x[i][j]='#';
		}
	}
}


void place_random_manager(int x, int y){
	int t=rand()%managers.size();
	int steps=0;
	while(ans[devs.size()+t].first!=-1){t++; steps++; if(t>=managers.size()) t=0;  if(steps>managers.size()) return;}
	ans[devs.size()+t].first=x; ans[devs.size()+t].second=y;
	placed[x][y]=t;
}

void place_random(int x, int y){
	int t=rand()%devs.size();
	int steps=0;
	while(ans[t].first!=-1){t++; if(t>=devs.size()) t=0; steps++; if(steps>devs.size()) return;}
	ans[t].first=x; ans[t].second=y;
	placed[x][y]=t;
}

void place_dev(int x, int y){
	vector<pii> neighbors;	
	if(x>0 && placed[x-1][y]!=-1) neighbors.push_back(make_pair(placed[x-1][y],ma3x[x-1][y]=='M'));
	if(y>0 && placed[x][y-1]!=-1) neighbors.push_back(make_pair(placed[x][y-1],ma3x[x][y-1]=='M'));

	if(neighbors.size()==0) return place_random(x,y);

	int max_score=0,cur_score=0;
	int max_score_index=-1;

	for(int i=0;i<devs.size();i++){
		if(ans[i].first!=-1) continue;
		cur_score=0;
		for(int j=0;j<neighbors.size();j++){
			if(neighbors[j].second)
			cur_score+=score_btw2(devs[i],managers[neighbors[j].first]);
			else cur_score+=score_btw2(devs[i],devs[neighbors[j].first]);
		}
		if(cur_score>=max_score){
			max_score=cur_score;
			max_score_index=i;
		}
	}
	if(max_score_index<0) return;
	
	placed[x][y]=max_score_index;
	//cerr<<"placing a dev on "<<x<<" "<<y<<" "<<max_score_index<<endl;
	ans[max_score_index]=make_pair(x,y);
	global_score+=max_score;
}

void place_manager(int x, int y){
	vector<pii> neighbors;
	if(x>0 && placed[x-1][y]!=-1) neighbors.push_back(make_pair(placed[x-1][y],ma3x[x-1][y]=='M'));
	if(y>0 && placed[x][y-1]!=-1) neighbors.push_back(make_pair(placed[x][y-1],ma3x[x][y-1]=='M'));

	if(neighbors.size()==0) return place_random_manager(x,y);

	int max_score=0,cur_score=0;
	int max_score_index=-1;
	for(int i=0;i<managers.size();i++){
		cur_score=0;
		if(ans[devs.size()+i].first!=-1) continue;
		for(int j=0;j<neighbors.size();j++){
			if(neighbors[j].second)
			cur_score+=score_btw2(managers[i],managers[neighbors[j].first]);
			else cur_score+=score_btw2(managers[i],devs[neighbors[j].first]);
		}
		
		if(cur_score>=max_score){
			max_score=cur_score;
			max_score_index=i;
		}
	}
	if(max_score_index<0) return;
	placed[x][y]=max_score_index;
	//cerr<<"placing a manager on "<<x<<" "<<y<<" "<<devs.size()+max_score_index<<endl;
	ans[devs.size()+max_score_index]=make_pair(x,y);
	global_score+=max_score;
}

void solve(){
	//for(int i=0;i<devs.size();i++) devvs.insert(devs[i]);
	memset(placed,-1,sizeof(int)*1000*1000);
	ans.resize(devs.size()+managers.size());
	for(int i=0;i<ans.size();i++) ans[i]=make_pair(-1,-1);
	for(int i=0;i<n;i++){
		for(int j=0;j<m;j++){
			if(ma3x[i][j]=='_'){
				place_dev(i,j);
			}
			if(ma3x[i][j]=='M'){
				place_manager(i,j);
			}
		}
		//cerr<<i<<endl;
	}		
}


void output(){
	//if(ANNEALING_FEED) return printState();
	//if(DEBUG_PRINT) return printScore();
	//make_ans();
	for(int i=0;i<devs.size()+managers.size();i++){
		if(ans[i].first==-1) cout<<"X"<<endl;
		else cout<<ans[i].second<<" "<<ans[i].first<<endl;
	}
	cerr<<global_score<<endl;
}

void input(){
	//freopen(".in","r",stdin);
	//freopen(".out","w",stdout);
	//cin.sync_with_stdio(0);
	//cin.tie(0);
	int c,cc;
	string temp;
	cin>>m>>n;
	ma3x.resize(n);
	for(int i=0;i<n;i++){
		cin>>ma3x[i];
	}
	filter_map();
	cin>>c;
	unordered_map<string,int> companies_house;
	unordered_map<string,int> skills;
	devs.resize(c);
	for(int i=0;i<c;i++){
		cin>>temp;
		if(companies_house.find(temp)==companies_house.end()) companies_house.insert(make_pair(temp,companies_house.size()));
		devs[i].c=companies_house[temp];
		cin>>devs[i].b>>cc;
		for(int j=0;j<cc;j++) {
			cin>>temp;
			if(skills.find(temp)==skills.end()) skills.insert(make_pair(temp,skills.size()));
			devs[i].skills.insert(skills[temp]);
		}
	}
	cin>>c;
	managers.resize(c);
	for(int i=0;i<c;i++){
		cin>>temp;
		if(companies_house.find(temp)==companies_house.end()) companies_house.insert(make_pair(temp,companies_house.size()));
		managers[i].c=companies_house[temp];
		cin>>managers[i].b;
	}
}

int main()
{
	input();
	solve();
	output();
	return 0;
}