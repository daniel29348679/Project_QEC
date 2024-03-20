# include <cstdlib>
# include <stdio.h>
# include <iostream>
# include <vector>
# include <string>
# include <sstream>
# include <map>
# include <stdexcept>
# include <iomanip>
# include <cstring>
using namespace std;


class Token {
public:
	string mtype;
	string mdata;
	Token() {
	}


	Token(string str) { //不會有空格
		mdata = str;
		if(str == "*" || str == "/" || str == "+" || str == "-") {
			mtype = "arith";
		} // if
		else if(str == ":=") {
			mtype = "assign";
		} // else if
		else if(str == "=" || str == "<>" || str == "<" || str == ">" || str == "<=" || str == ">=") {
			mtype = "boolean_opt";
		} // else if
		else if(str[0] == '.' || (str[0] >= '0' && str[0] <= '9')) {
			mtype = "num";
		} // else if
		else if((str[0] >= 'a' && str[0] <= 'z') || (str[0] >= 'A' && str[0] <= 'Z')) {
			mtype = "IDENT";
		} // else if
		else if(str == "(") {
			mtype = "left";
		} // else if
		else if(str == ")") {
			mtype = "right";
		}
		else {
			throw runtime_error("R U STUPID OR SOMETHING I just said NO PRANK ON ME you IDIOT");
		}
	}     // Token()


	void Modifytype(string str) {
		mtype = str;
	}


	string Gettype() {
		return mtype;
	}


	string Getdata() {
		return mdata;
	}


	//寫一些token會用到的function
}; // Class Token


class Operand {
public:
	// 有可能是5或5.5或a=1.5或a=1 (變數的int跟float和數字的int跟float)
	string variablename = "";
	string variabletype = "";
	int intnum			= 0;
	float floatnum		= 0;
	bool boolean		= 0;


	Operand() {
	}


	Operand(bool b) {
		boolean		 = b;
		variabletype = "boolean";
	}


	Operand(int num) {
		intnum		 = num;
		variabletype = "int";
	}


	Operand(float num) {
		floatnum	 = num;
		variabletype = "float";
	}


	Operand(string name, bool b) {
		boolean		 = b;
		variablename = name;
		variabletype = "boolean";
	}


	Operand(string name, int num) {
		intnum		 = num;
		variablename = name;
		variabletype = "int";
	}


	Operand(string name, float num) {
		floatnum	 = num;
		variablename = name;
		variabletype = "float";
	}


	float Evaluate(float a, float b, char op) {
		// cout << fixed << setprecision(3) << 3.1234 << endl;
		// cout << ans; //bool/int/float
		return 0;
	}


	float Evaluate(int a, float b, char op) {
		// cout << fixed << setprecision(3) << 3.1234 << endl;
		// cout << ans; //bool/int/float
		return 0;
	}


	float Evaluate(float a, int b, char op) {
		// cout << fixed << setprecision(3) << 3.1234 << endl;
		// cout << ans; //bool/int/float
		return 0;
	}


	int Evaluate(int a, int b, char op) {
		return 0;
	}


	bool IsItTrue(int a, int b, char cmp_op) {
		return 0; // 敘述式是否成立
	}


	string Getname() {
		return variablename;
	}
};


bool Check(Token a, Token b);


void Cut(string str, bool isend) {
	if(str == "") {
		return;
	}
	int pair = 0;
	//遍歷整個str檢測第一型錯誤(一次一個字元)
	for(int i = 0; i < str.size(); i++) {
		//數字a-zA-Z()+-*/._><=空格:=
		if(str[i] == '+' || str[i] == '-' || str[i] == '*' || str[i] == '/' ||
		   str[i] == '=' || str[i] == '<' || str[i] == '>' || str[i] == '.' ||
		   (str[i] >= '0' && str[i] <= '9') || str[i] == '_' || (str[i] >= 'a' && str[i] <= 'z') ||
		   (str[i] >= 'A' && str[i] <= 'Z') || str[i] == '(' || str[i] == ')' || str[i] == ' ') { // +-有可能是正負 /註解在main會處理掉
			// 合法字元
			if(str[i] == '(') {
				pair++;
			}
			if(str[i] == ')') {
				pair--;
			}
			if(pair < 0) {
				throw runtime_error("Unexpected token : ')'");
			}
		} // if
		else if(i < str.size() - 1 && str.substr(i, 2) == ":=") { // :不是最後一個且後面是=
			// 合法
			i++;                                                  //因為一次看兩個字所以要i++
		} // else if
		else {                                                    // 不合法
			//遞迴錯誤字元以前的東西????
			throw runtime_error("Unrecognized token with first char : '" + str.substr(i, 1) + "'");
		} // else
	}
	if(pair != 0) {
		throw runtime_error("Unrecognized token with first char : ';(((('");
	}

	Token tokens[1000];
	int	  tokens_size = 0;
	bool  assign	  = 0;

	//切token + 檢測第二型錯誤(文意)(一次多個字元為一個token)
	//跳過空格??
	for(int i = 0; i < str.size();) {
		if(str.substr(i, 1) == " ") {
			i++;
		}
		//2
		else if(str.substr(i, 2) == "<=" || str.substr(i, 2) == ">=" ||
				str.substr(i, 2) == "<>" || str.substr(i, 2) == ":=") {
			if(assign && str.substr(i, 2) == ":=") {
				throw runtime_error("Unexpected token : ':='");
			}
			if(str.substr(i, 2) == ":=") {
				//assign符號很特殊不能出現兩次所以文法上要特別處理
				assign = 1;
			}

			Token tk(str.substr(i, 2));
			tokens[tokens_size] = tk;
			tokens_size++;
			i += 2;
		}
		//1
		else if(str.substr(i, 1) == "<" || str.substr(i, 1) == ">" || str.substr(i, 1) == "+" ||
				str.substr(i, 1) == "-" || str.substr(i, 1) == "*" || str.substr(i, 1) == "/" ||
				str.substr(i, 1) == "(" || str.substr(i, 1) == ")" || str.substr(i, 1) == "=") {
			//+-*/=()><
			Token tk(str.substr(i, 1));
			tokens[tokens_size] = tk;
			if(tokens_size == 0 && (str.substr(i, 1) == "+" || str.substr(i, 1) == "-")) {
				tokens[tokens_size].Modifytype("sign");
			}
			if((tokens_size > 0) && (str.substr(i, 1) == "+" || str.substr(i, 1) == "-") &&
			   (tokens[tokens_size - 1].Gettype() == "arith" || tokens[tokens_size - 1].Gettype() == "left" ||
				tokens[tokens_size - 1].Gettype() == "assign" || tokens[tokens_size - 1].Gettype() == "boolean_opt")) {
				tokens[tokens_size].Modifytype("sign");
			}
			tokens_size++;
			i++;
		}
		//數字小數點
		else if((str[i] >= '0' && str[i] <= '9') || str[i] == '.') {
			int mode = 1;
			if(str[i] == '.') {
				mode--;
			}
			string number = "";
			string wrong  = "";
			number += str[i];
			i++;
			while(mode > -2 && (str[i] == '.' || (str[i] >= '0' && str[i] <= '9')) && i < str.size()) {
				if(str[i] == '.') {
					if(mode == 1) {
						number += str[i];
					}
					else if(mode == 0) {
						wrong += str[i];
					}
					mode--; //變0 -1 -2
				}
				else if(str[i] >= '0' && str[i] <= '9') {
					if(mode == 1) {
						number += str[i];
					}
					else if(mode == 0) {
						number += str[i];
					}
					else if(mode == -1) {
						wrong += str[i];
					}
				}
				else {
					cout << "i >= str.size(?)";
				}
				//mode=-1錯誤模式 遇到數字給wrong 欲到小數點跳while 並印錯中斷
				//mode=0分數模式 遇到數字給number 欲到小數點給wrong進入錯誤模式 其他跳while成功
				//mode=1正常模式 遇到數字給number 欲到小數點給number進入分數模式 其他跳while成功
				i++;
			} // while
			if(mode == -1) {
				throw runtime_error("Unexpected token : '" + wrong + "'");
			}
			if(number == ".") {
				throw runtime_error("Unrecognized token with first char : '.'");
			}
			Token tk(number);
			tokens[tokens_size] = tk;
			tokens_size++;
		}
		//AZ_az
		else if(str[i] == '_') {
			throw runtime_error("Unrecognized token with first char : '_'");
		}
		else if((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z')) {
			string variable;
			variable += str[i];
			i++;
			while((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z') || str[i] == '_' || (str[i] >= '0' && str[i] <= '9')) {
				variable += str[i];
				i++;
			}
			Token tk(variable);
			tokens[tokens_size] = tk;
			tokens_size++;
		}
	} // for

	// 丟進check做前後文法檢查
	for(int i = 0; i < tokens_size - 1 ; i++) {
		if(!Check(tokens[i], tokens[i + 1])) {
			throw runtime_error("Unexpected token : '" + tokens[i + 1].Getdata() + "'");
		}
	}

	//這次丟進來檢查是因為分號的話
	if(isend) {
		//cout << "check because ';'\n";
		//cout << tokens[tokens_size - 1].Gettype();
		cout << tokens[tokens_size - 1].Gettype();
		cout << tokens[tokens_size - 1].Getdata();
		if(!(tokens[tokens_size].Gettype() == "num" || tokens[tokens_size].Gettype() == "IDENT" || tokens[tokens_size].Gettype() == "right")) {
			cout << "\nwrong!!\n";
			throw runtime_error("Unexpected token : ';'");     // !!!!!!!!!!!!!!!
		}
	}

	cout << str << ":correct\n";

	// 若不是end就不用計算
	Operand operands[1000]; // 存被乘數和宣告過的operand之類的
	int		numOfoperands = 0;

	// 判斷是運算元or運算子 並 依序計算
	for(int i = 0; i <= tokens_size - 1 ; i++) {
		// cout << tokens[i].Getdata() << endl;
		// token裡有些名詞沒宣告過，可去查Operand型別的array
		// 注意先乘除後加減和括號
		// 呼叫Operand內建函式Evaluate()們

		// 未宣告過的報錯
		if(tokens[i].Gettype() == "IDENT") {
			bool   find	  = 0;
			string newvar = tokens[i].Getdata();
			for(int i = 0; i < numOfoperands && !find; i++) {
				if(strcmp(operands[numOfoperands].Getname(), newvar) == 0) {
					find = 1;
				}
			}
			if(!find) {
				throw runtime_error("Undefided identifier : '" + newvar + "'");
			}
		}

		// 宣告變數
		if(tokens[i].Getdata() == ":=") {
			Operand vari(tokens[i - 1], tokens[i + 1]);
			operands[numOfoperands] = vari;
			numOfoperands++;
		}

		//
		if(tokens[i].Gettype() == "boolean_opt") {
		}
	}


	//throw runtime_error("Unexpected token : '" + str.substr(0, 1) + "'");
	//semantic error(Undefided identifier)變數未宣告
	//throw runtime_error("Undefided identifier : '" + str.substr(0, 1) + "'");
} // Cut()


bool Check(Token a, Token b) {
	if(a.Gettype() == "sign" && b.Gettype() == "num") {
		return 1;
	}
	if(a.Gettype() == "left" &&
	   (b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num")) {
		return 1;
	}
	if(a.Gettype() == "right" &&
	   (b.Gettype() == "arith" || b.Gettype() == "right" || b.Gettype() == "boolean_opt")) {
		return 1;
	}
	if(a.Gettype() == "assign" &&
	   (b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num" || b.Gettype() == "IDENT")) {
		return 1;
	}
	if(a.Gettype() == "num" &&
	   (b.Gettype() == "arith" || b.Gettype() == "boolean_opt" || b.Gettype() == "right")) {
		return 1;
	}
	if(a.Gettype() == "IDENT" &&
	   (b.Gettype() == "arith" || b.Gettype() == "boolean_opt" || b.Gettype() == "right")) {
		return 1;
	}
	if(a.Gettype() == "boolean_opt" &&
	   (b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num")) {
		return 1;
	}
	if(a.Gettype() == "arith" &&
	   (b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num" || b.Gettype() == "IDENT")) {
		return 1;
	}
	return 0;
}


int main() {
	//getchar()

	string utestnum;

	cin >> utestnum;
	if(utestnum == "quit") {
		cout << "Program exits...because utestnum\n";
		return 0;
	}
	cout << "Program starts...\n";
	getchar();


	bool scrapline = 0;

	while(1) {
		scrapline = 0;
		try{
			string str			  = "";
			char   c			  = ' ';
			bool   alreadyHasADiv = 0;
			bool   graywords	  = 0;
			c = getchar(); // 獨到前一行最後的enter
			while(c != ';') {
				if(str == "quit") {
					cout << "Program exits...";
					return 0;
				}
				if(!graywords) {
					if(c == '/') {
						if(alreadyHasADiv) {
							graywords = 1;
							// alreadyHasADiv = 0;
						}
						else {
							alreadyHasADiv = 1;
						}
					}
					else {
						if(alreadyHasADiv) {
							alreadyHasADiv = 0;
							//在這裡才知道前一個是除不是註解 所以現在才加前一個(/)進str
							str += '/';
						}
					}

					if(c != ' ' && c != '\n' && c != '\t' && c != '/') { //加本人
						str += c;
					}
					if(c == '\n' || c == ' ') {
						str += ' ';
						if(c == ' ') {
							scrapline = 1;
						}
						//cout << "check" << str << " ";
						Cut(str, 0); // function裡有1000格token
						//沒分號直接按enter的話還是要檢測文法錯
						//如果檢測發現是錯的就會跳走但後面再錯都不要理
					}
				} // if
				if(c == '\n') {
					graywords = false;
					//註解域到換行 解除註解
				}
				c = getchar();
				if(c == ';') {
					scrapline = 1;
				}
			} // while
			  //把第一個;以前的str略過註解和換行保留空格，放進Check(str);
			if(str == "quit") {
				cout << "Program exits....\n";
				return 0;
			}
			Cut(str, 1);
			//Evaluate();
		}     // try
		catch(runtime_error&e) {
			cout << "> " << e.what() << endl;
			if(scrapline) {
				//因為空格;所以遇到檢查 所以發現錯誤跳來這的 其實後面還有
				while(getchar() != '\n') {
					;
				}
			}
		} // catch
	}     // while 處理每次指令
}         // main


// 3/0?
// quit
