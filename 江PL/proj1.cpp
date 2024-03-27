# include <cstdlib>
# include <stdio.h>
#include <stdlib.h>
# include <iostream>
# include <vector>
# include <string>
# include <sstream>
# include <map>
# include <stdexcept>
# include <iomanip>
# include <cstring>
#include <stack>
using namespace std;


class Token {
public:
  string mtype;
  string mdata;
  Token() {
  } // Token()

  Token( string str ) { // 不會有空格
    mdata = str;
    if ( str == "*" || str == "/" || str == "+" || str == "-" )
      mtype = "arith";
    // if
    else if ( str == ":=" )
      mtype = "assign";
    // else if
    else if ( str == "=" || str == "<>" || str == "<" || str == ">" || str == "<=" || str == ">=" )
      mtype = "boolean_opt";
    // else if
    else if ( str[ 0 ] == '.' || ( str[ 0 ] >= '0' && str[ 0 ] <= '9' ) )
      mtype = "num";
    // else if
    else if ( ( str[ 0 ] >= 'a' && str[ 0 ] <= 'z' ) || ( str[ 0 ] >= 'A' && str[ 0 ] <= 'Z' ) )
      mtype = "IDENT";
    // else if
    else if ( str == "(" )
      mtype = "left";
    // else if
    else if ( str == ")" )
      mtype = "right";
    else
      throw runtime_error( "R U STUPID OR SOMETHING I just said NO PRANK ON ME you IDIOT" );
  }     // Token()

  void Modifytype( string str ) {
    mtype = str;
  } // Modifytype()

  string Gettype() {
    return mtype;
  } // Gettype()

  string Getdata() {
    return mdata;
  } // Getdata()

  // 寫一些token會用到的function
}; // Class Token

int Isfloat( string str ) {
  for ( int i = 0 ; i < str.size() ; i++ )
    if ( str[ i ] == '.' ) return 2;

  return 1;
} // Isfloat()

class Operand {
public:
  // 有可能是5或5.5或a=1.5或a=1 (變數的int跟float和數字的int跟float)
  string mvariablename;
  string mvariabletype;
  int mintnum;
  float mfloatnum;
  bool mbooleannum;

  Operand() {
  } // Operand()

  // 不會有人宣告布林變數
  Operand( int num ) {
    mintnum       = num;
    mvariabletype = "int";
    mbooleannum   = 0;
    mfloatnum     = 0;
  } // Operand()

  Operand( float num ) {
    mfloatnum     = num;
    mintnum       = 0;
    mbooleannum   = 0;
    mvariabletype = "float";
  } // Operand()

  // 讀token的時候是讀到string所以丟進Operand也是string要可以用
  Operand( string name, string num ) {
    mvariablename = name;
    if ( Isfloat( num ) == 2 ) {
      // float
      mfloatnum     = atof( num.c_str() );
      mvariabletype = "float";
      mintnum       = 0;
      mbooleannum   = 0;
    } // if
    else if ( Isfloat( num ) == 1 ) {
      // int
      mvariabletype = "int";
      mintnum       = atoi( num.c_str() );
      mfloatnum     = 0;
      mbooleannum   = 0;
    } // else if
    else
      cout << "NOT FLOAT NOR INT...";
  } // Operand()

  string Getvarname() {
    return mvariablename;
  } // Getvarname()

  float Getvarvaluef() {
    return mfloatnum;
  } // Getvarvaluef()

  int Getvarvaluei() {
    return mintnum;
  } // Getvarvaluei()

  string Getvartype() {
    return mvariabletype;
  } // Getvartype()

  void Setvalue( string value ) {
    if ( Isfloat( value ) ) {
      mfloatnum     = atof( value.c_str() );
      mvariabletype = "float";
      mintnum       = 0;
      mbooleannum   = 0;
    } // if
    else {
      mvariabletype = "int";
      mintnum       = atoi( value.c_str() );
      mfloatnum     = 0;
      mbooleannum   = 0;
    } // else
  }   // Setvalue()
};

// 記憶體將重複使用，所以要有指標指向適當的起始位置
Token gtokens[ 1000 ];
int   gtokens_size = 0;
int   gtoken_start = 0; // 起始位置
bool  gassign      = 0;

Operand goperands[ 1000 ];  // 存宣告過的變數(記憶體)
int     gnumOfoperands = 0;
int     goperand_start = 0; // 起始位置


// 敘述式是否成立
// 可能是float跟int比??
bool IsItTrue( Operand a, Operand b, string cmp_op ) {
  // 左右都已經算出一個Operand值了，簡單比大小就好
  if ( cmp_op.compare( "<" ) == 0 ) {
    if ( a.Getvartype() == "int" && b.Getvartype() == "int" )
      return a.Getvarvaluei() < b.Getvarvaluei();

    if ( a.Getvartype() == "float" && b.Getvartype() == "int" )
      return a.Getvarvaluef() < b.Getvarvaluei();

    if ( a.Getvartype() == "int" && b.Getvartype() == "float" )
      return a.Getvarvaluei() < b.Getvarvaluef();

    if ( a.Getvartype() == "float" && b.Getvartype() == "float" )
      return a.Getvarvaluef() < b.Getvarvaluef();
  } // if
  if ( cmp_op.compare( "<=" ) == 0 ) {
    if ( a.Getvartype() == "int" && b.Getvartype() == "int" )
      return a.Getvarvaluei() <= b.Getvarvaluei();

    if ( a.Getvartype() == "float" && b.Getvartype() == "int" )
      return a.Getvarvaluef() <= b.Getvarvaluei();

    if ( a.Getvartype() == "int" && b.Getvartype() == "float" )
      return a.Getvarvaluei() <= b.Getvarvaluef();

    if ( a.Getvartype() == "float" && b.Getvartype() == "float" )
      return a.Getvarvaluef() <= b.Getvarvaluef();
  } // if
  if ( cmp_op.compare( ">" ) == 0 ) {
    if ( a.Getvartype() == "int" && b.Getvartype() == "int" )
      return a.Getvarvaluei() > b.Getvarvaluei();

    if ( a.Getvartype() == "float" && b.Getvartype() == "int" )
      return a.Getvarvaluef() > b.Getvarvaluei();

    if ( a.Getvartype() == "int" && b.Getvartype() == "float" )
      return a.Getvarvaluei() > b.Getvarvaluef();

    if ( a.Getvartype() == "float" && b.Getvartype() == "float" )
      return a.Getvarvaluef() > b.Getvarvaluef();
  } // if
  if ( cmp_op.compare( ">=" ) == 0 ) {
    if ( a.Getvartype() == "int" && b.Getvartype() == "int" )
      return a.Getvarvaluei() >= b.Getvarvaluei();

    if ( a.Getvartype() == "float" && b.Getvartype() == "int" )
      return a.Getvarvaluef() >= b.Getvarvaluei();

    if ( a.Getvartype() == "int" && b.Getvartype() == "float" )
      return a.Getvarvaluei() >= b.Getvarvaluef();

    if ( a.Getvartype() == "float" && b.Getvartype() == "float" )
      return a.Getvarvaluef() >= b.Getvarvaluef();
  } // if
  if ( cmp_op.compare( "<>" ) == 0 ) {
    if ( a.Getvartype() == "int" && b.Getvartype() == "int" )
      return a.Getvarvaluei() != b.Getvarvaluei();

    if ( a.Getvartype() == "float" && b.Getvartype() == "int" )
      return a.Getvarvaluef() != b.Getvarvaluei();

    if ( a.Getvartype() == "int" && b.Getvartype() == "float" )
      return a.Getvarvaluei() != b.Getvarvaluef();

    if ( a.Getvartype() == "float" && b.Getvartype() == "float" )
      return a.Getvarvaluef() != b.Getvarvaluef();
  } // if
  if ( cmp_op.compare( "=" ) == 0 ) {
    if ( a.Getvartype() == "int" && b.Getvartype() == "int" )
      return a.Getvarvaluei() == b.Getvarvaluei();

    if ( a.Getvartype() == "float" && b.Getvartype() == "int" )
      return a.Getvarvaluef() == b.Getvarvaluei();

    if ( a.Getvartype() == "int" && b.Getvartype() == "float" )
      return a.Getvarvaluei() == b.Getvarvaluef();

    if ( a.Getvartype() == "float" && b.Getvartype() == "float" )
      return a.Getvarvaluef() == b.Getvarvaluef();
  } // if
  cout << "\n IsItTrue() wrong!\n";
  return 0;
}   // IsItTrue()

bool Check( Token a, Token b ) {
  if ( a.Gettype() == "sign" && b.Gettype() == "num" )
    return 1;

  if ( a.Gettype() == "left" &&
       ( b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num" ) )
    return 1;

  if ( a.Gettype() == "right" &&
       ( b.Gettype() == "arith" || b.Gettype() == "right" || b.Gettype() == "boolean_opt" ) )
    return 1;

  if ( a.Gettype() == "assign" &&
       ( b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num" || b.Gettype() == "IDENT" ) )
    return 1;

  if ( a.Gettype() == "num" &&
       ( b.Gettype() == "arith" || b.Gettype() == "boolean_opt" || b.Gettype() == "right" ) )
    return 1;

  if ( a.Gettype() == "IDENT" &&
       ( b.Gettype() == "arith" || b.Gettype() == "boolean_opt" || b.Gettype() == "right" || b.Gettype() == "assign" ) )
    return 1;

  if ( a.Gettype() == "boolean_opt" &&
       ( b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num" ) )
    return 1;

  if ( a.Gettype() == "arith" &&
       ( b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num" || b.Gettype() == "IDENT" ) )
    return 1;

  return 0;
} // Check()

bool Hasdeclared( string varname ) {
  bool find = 0;

  for ( int k = 0 ; k < gnumOfoperands && ! find ; k++ )
    if ( varname.compare( goperands[ k ].Getvarname() ) == 0 )
      find = 1;

  if ( ! find ) return false;
  else return true;
} // Hasdeclared()

string ToStr( Operand a ) {
  stringstream oss;

  if ( a.Getvartype() == "float" ) {
    oss << fixed << setprecision( 3 ) << a.Getvarvaluef();
    return oss.str();
  } // if
  else if ( a.Getvartype() == "int" ) {
    oss << a.Getvarvaluei();
    return oss.str();
  }   // else if
  else
    return a.Getvarname() + "is not float nor int\n";
} // ToStr()

bool OnlyNumber( int start, int end ) {
  for ( int i = start ; i <= end ; i++ )
    if ( gtokens[ i ].Gettype() != "num" ) return false;

  // for
  return true;
} // OnlyNumber()

bool OnlyIDENT( int start, int end ) {
  for ( int i = start ; i <= end ; i++ )
    if ( gtokens[ i ].Gettype() != "num" ) return false;

  // for
  return true;
} // OnlyIDENT()

// 遍歷整個str檢測第一型錯誤(一次一個字元)(加到全域變數gtokens會重複!有可能是換行的str!)
void Cut( string str, bool isend ) {
  if ( str.compare( "" ) == 0 )
    return;

  int apair = 0;
  for ( int i = 0 ; i < str.size() ; i++ ) {
    // 數字a-zA-Z()+-*/._><=空格:=
    if ( str[ i ] == '+' || str[ i ] == '-' || str[ i ] == '*' || str[ i ] == '/' ||
         str[ i ] == '=' || str[ i ] == '<' || str[ i ] == '>' || str[ i ] == '.' ||
         ( str[ i ] >= '0' && str[ i ] <= '9' ) || str[ i ] == '_' ||
         ( str[ i ] >= 'a' && str[ i ] <= 'z' ) || ( str[ i ] >= 'A' && str[ i ] <= 'Z' ) ||
         str[ i ] == '(' || str[ i ] == ')' || str[ i ] == ' ' ) {   // +-有可能是正負 /註解在main會處理掉
      // 合法字元
      if ( str[ i ] == '(' )
        apair++;
      if ( str[ i ] == ')' )
        apair--;
      if ( apair < 0 )
        throw runtime_error( "Unexpected token : ')'305" );
    } // if
    else if ( i < str.size() - 1 && str.substr( i, 2 ) == ":=" ) { // :不是最後一個且後面是=
      // 合法
      i++;                                                  // 因為一次看兩個字所以要i++
    } // else if
    else                                                    // 不合法
      // 遞迴錯誤字元以前的東西????
      throw runtime_error( "Unrecognized token with first char : '" + str.substr( i, 1 ) + "'313" );
    // else
  } // for

  if ( apair != 0 && isend )
    throw runtime_error( "Unexpected token : ';357'" ); // 括號不成對卻已經遇到;


  // 切token + 檢測第二型錯誤(文意)(一次多個字元為一個token)
  // 跳過空格??
  for ( int i = 0 ; i < str.size() ;) {
    if ( str.substr( i, 1 ) == " " )
      i++;

    else if ( str.substr( i, 2 ) == "<=" || str.substr( i, 2 ) == ">=" ||
              str.substr( i, 2 ) == "<>" || str.substr( i, 2 ) == ":=" ) {
      if ( gassign && str.substr( i, 2 ) == ":=" )
        throw runtime_error( "Unexpected token : ':='369" );  // 出現重複的:=
      if ( str.substr( i, 2 ) == ":=" )
        // assign符號很特殊不能出現兩次所以文法上要特別處理
        gassign = 1;

      // 加進gtokens
      Token tk( str.substr( i, 2 ) );
      gtokens[ gtokens_size ] = tk;
      gtokens_size++;

      i += 2;
    }   // else if

    else if ( ( str.substr( i, 1 ) == "<" || str.substr( i, 1 ) == ">" || str.substr( i, 1 ) == "+" ||
                str.substr( i, 1 ) == "-" || str.substr( i, 1 ) == "*" || str.substr( i, 1 ) == "/" ||
                str.substr( i, 1 ) == "(" || str.substr( i, 1 ) == ")" || str.substr( i, 1 ) == "=" )  ) {
      // +-*/=()><

      Token tk( str.substr( i, 1 ) );
      gtokens[ gtokens_size ] = tk;
      if ( gtokens_size - gtoken_start == 0 && ( str.substr( i, 1 ) == "+" || str.substr( i, 1 ) == "-" ) )
        gtokens[ gtokens_size ].Modifytype( "sign" );
      if ( ( gtokens_size > 0 ) && ( str.substr( i, 1 ) == "+" || str.substr( i, 1 ) == "-" ) &&
           ( gtokens[ gtokens_size - 1 ].Gettype() == "arith" || gtokens[ gtokens_size - 1 ].Gettype() == "left" ||
             gtokens[ gtokens_size - 1 ].Gettype() == "assign" ||
             gtokens[ gtokens_size - 1 ].Gettype() == "boolean_opt" ) )
        gtokens[ gtokens_size ].Modifytype( "sign" );
      gtokens_size++;

      i++;
    } // else if
    // 數字小數點
    else if (  ( ( str[ i ] >= '0' && str[ i ] <= '9' ) || str[ i ] == '.' ) ) {
      int mode = 1;
      if ( str[ i ] == '.' )
        mode--;
      string number = "";
      string wrong  = "";
      number += str[ i ];
      i++;
      while ( mode > -2 && ( str[ i ] == '.' || ( str[ i ] >= '0' && str[ i ] <= '9' ) ) &&
              i < str.size() ) {
        if ( str[ i ] == '.' ) {
          if ( mode == 1 )
            number += str[ i ];
          else if ( mode == 0 )
            wrong += str[ i ];
          mode--; // 變0 -1 -2
        } // if
        else if ( str[ i ] >= '0' && str[ i ] <= '9' ) {
          if ( mode == 1 )
            number += str[ i ];
          else if ( mode == 0 )
            number += str[ i ];
          else if ( mode == -1 )
            wrong += str[ i ];
        } // else if
        else
          cout << "i >= str.size(?)";
        // mode=-1錯誤模式 遇到數字給wrong 欲到小數點跳while 並印錯中斷
        // mode=0分數模式 遇到數字給number 欲到小數點給wrong進入錯誤模式 其他跳while成功
        // mode=1正常模式 遇到數字給number 欲到小數點給number進入分數模式 其他跳while成功
        i++;
      } // while
      if ( mode == -1 )
        throw runtime_error( "Unexpected token : '" + wrong + "'394" );
      if ( number == "." )
        throw runtime_error( "Unrecognized token with first char : '.'" );
      Token tk( number );
      gtokens[ gtokens_size ] = tk;
      gtokens_size++;
    } // else if
    // AZ_az
    else if ( str[ i ] == '_' )
      throw runtime_error( "Unrecognized token with first char : '_'" );
    else if (  ( ( str[ i ] >= 'a' && str[ i ] <= 'z' ) || ( str[ i ] >= 'A' && str[ i ] <= 'Z' ) ) ) {
      string variable;
      variable += str[ i ];
      i++;
      while ( ( str[ i ] >= 'a' && str[ i ] <= 'z' ) || ( str[ i ] >= 'A' && str[ i ] <= 'Z' ) ||
              str[ i ] == '_' || ( str[ i ] >= '0' && str[ i ] <= '9' ) ) {
        variable += str[ i ];
        i++;
      } // while
      Token tk( variable );
      gtokens[ gtokens_size ] = tk;
      gtokens_size++;
    } // else if
  }   // for


  if ( gtokens[ gtokens_size - 1 ].Getdata() == "quit" ) {
    cout << "Program exits...458\n";
    exit( 0 );
  } // if

  // 遍歷token (丟進check)
  for ( int i = gtoken_start ; i <= gtokens_size - 2 ; i++ )
    if ( isend && ! Check( gtokens[ i ], gtokens[ i + 1 ] ) )
      throw runtime_error( "Unexpected token : '" + gtokens[ i + 1 ].Getdata() + "'466" );
  // if
  // for

  // 這次丟進來檢查是因為分號的話
  if ( isend )
    if ( ! ( gtokens[ gtokens_size - 1 ].Gettype() == "num" || gtokens[ gtokens_size - 1 ].Gettype() == "IDENT" ||
             gtokens[ gtokens_size - 1 ].Gettype() == "right" ) )
      throw runtime_error( "Unexpected token : ';'473" );
  // if

  // for ( int i = gtoken_start ; i <= gtokens_size - 1 ; i++ )
  //   cout << gtokens[ i ].Getdata() << " " << gtokens[ i ].Gettype() << endl;
} // Cut()

// 某段指定的token是expression，要轉後序式並回傳答案(Operand)
// 要處理sign+num
Operand Evaluate( int start, int end ) {
  Operand ans;

  // 一個IDENT (宣告過)
  if ( start == end && gtokens[ start ].Gettype() == "IDENT" ) {
    string exp = gtokens[ start ].Getdata();
    ans.Setvalue( exp );
    return ans;
  } // if

  // 一個數字 -49.215是兩個token
  if ( ( start == end && gtokens[ start ].Gettype() == "num" ) ||
       ( end == start + 1 && gtokens[ start ].Gettype() == "sign" &&
         gtokens[ start ].Gettype() == "num" ) ) {
    string exp = gtokens[ start ].Getdata() + gtokens[ end ].Getdata();
    ans.Setvalue( exp );
    return ans;
  } // if

  // 一段exp算式(含IDENT)
  // 優先順序法
  std::stack<float> numstack;
  stack<char>       opstack;

  for ( int i = start ; i <= end ; i++ ) {
  } // for

  // 後序式求值
  int mode = 0;

  return ans;
} // Evaluate()

// 遍歷指定token範圍 找出:=和cmp_op
void Calculate() {
  Operand ans;
  int     sentence = -1; // 定義式0 判斷式1 計算式-1

  if ( gtoken_start > gtokens_size )
    cout << "token_start  > tokens_size!\n";
  // if
  if ( goperand_start > gnumOfoperands )
    cout << "operand_start > numOfoperands!\n";
  // if

  // gtoken_start  goperand_start;
  // 遍歷token
  for ( int i = gtoken_start ; i <= gtokens_size - 1 && sentence == -1 ; i++ ) {
    // 但凡讀到未宣告過的IDENT直接報錯
    if ( gtokens[ i ].Gettype() == "IDENT" && gtokens[ i + 1 ].Getdata() != ":=" &&
         ( ! Hasdeclared( gtokens[ i ].Getdata() ) ) )
      throw runtime_error( "Undefided identifier : '" +
                           gtokens[ i ].Getdata() + "'493" );

    // 讀到:=就是定義式 第i個是:=
    if ( gtokens[ i ].Getdata() == ":=" ) {
      if ( gtokens[ i - 1 ].Gettype() == "IDENT" )
        sentence = 0;
      else
        throw runtime_error( "Unexpected token : ':='500" );

      // 等號左邊的是名子
      string varname = gtokens[ i - 1 ].Getdata();
      // 等號右邊(直到分號為止都是exp)(若不是exp就throw)丟進Evaluate()會回傳一個Operand
      for ( int j = i + 1 ; j < gtokens_size ; j++ ) {
        if ( gtokens[ j ].Gettype() == "IDENT" && ( ! Hasdeclared( gtokens[ j ].Getdata() ) ) )
          // 讀到沒見過的
          throw runtime_error( "Undefided identifier : '" + gtokens[ j ].Getdata() + "'508" );
        if ( gtokens[ j ].Gettype() == "assign" || gtokens[ j ].Gettype() == "boolean_opt" )
          // 如果後面有> < >= <= <> = :=
          throw runtime_error( "Unexpected token : '" + gtokens[ j ].Getdata() + "'511" );
      } // for
      Operand var( varname, ToStr( Evaluate( i + 1, gtokens_size - 1 ) ) ); // 型別： string, string
      // 新增一格Operand
      goperands[ gnumOfoperands ] = var;
      gnumOfoperands++;
      i = gtokens_size; // 不用讀了 下一則指令謝謝
      // 存甚麼印甚麼
      cout << ToStr( Evaluate( i + 1, gtokens_size - 1 ) );
    } // if


    // 讀到boolean_opt就是敘述式 第i個token是boolean_opt
    if ( gtokens[ i ].Gettype() == "boolean_opt" ) {
      sentence = 1;
      // 抓boolean_opt左右
      // 直到分號為止都是exp(若不是exp就throw)丟進Evaluate()會回傳一個Operand
      for ( int j = i + 1 ; j < gtokens_size ; j++ ) {
        // 剩餘exp還是有可能讀到沒見過的
        if ( gtokens[ j ].Gettype() == "IDENT" && ( ! Hasdeclared( gtokens[ j ].Getdata() ) ) )
          throw runtime_error( "Undefided identifier : '" + gtokens[ j ].Getdata() + "'510" );
        if ( gtokens[ j ].Gettype() == "assign" || gtokens[ j ].Gettype() == "boolean_opt" )
          throw runtime_error( "Unexpected token : '" + gtokens[ j ].Getdata() + "'551" );
      } // for
      // i+1~j-1是rightval
      // token_start~i-1是leftval
      IsItTrue( Evaluate( gtoken_start, i - 1 ), Evaluate( i + 1, gtokens_size - 1 ), gtokens[ i ].Getdata() ); // 203
      // 拿著token片段計算並比較
      i = gtokens_size;
    } // if

    // 是數字 IDENT sign arith ()就繼續數i
  }   // for跑完即判斷完成

  if ( sentence == 0 ) {
    // 定義式 for裡面new完了這裡不用做事
  } // if


  if ( sentence == 1 )
    // 印IsItTrue()的答案
    ;


  if ( sentence == -1 ) {
    // 計算式152
    // token_start~i-1是exp範圍
    // Evaluate(token_start, i-1)得出一個Operand
  }     // if
} // Calculate()

int main() {
  // getchar()

  string utestnum;

  cin >> utestnum;
  if ( utestnum == "quit" ) {
    cout << "Program exits...because utestnum\n";
    return 0;
  }
  cout << "Program starts...\n";
  // 記憶體啟用
  getchar();

  bool scrapline = 0;

  while ( 1 ) {
    gtoken_start = gtokens_size;
    // goperand_start = gnumOfoperands;
    scrapline = 0;
    try{
      string str            = "";
      char   c              = ' ';
      bool   alreadyHasADiv = 0;
      bool   graywords      = 0;
      c = getchar(); // 讀到前一行最後的enter
      // cout << "c='" << c << "'" << endl;
      while ( c != ';' ) {
        if ( str == "quit" ) {
          cout << "Program exits...629";
          return 0;
        } // if
        if ( ! graywords ) {
          if ( c == '/' ) {
            if ( alreadyHasADiv ) { // 讀到第二個除
              graywords = 1;
              str.pop_back();       // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!看起來很像vector
            } // if
            else {
              alreadyHasADiv = 1; // 讀到第一個除 先當他是除法
              str           += '/';
            } // else
          }      // if

          else { // c不是除
            if ( alreadyHasADiv )
              alreadyHasADiv = 0;
            // if

            if ( c != ' ' && c != '\n' ) // 加本人
              str += c;
          } // else


          if ( c == '\n' || c == ' ' ) {
            str += ' ';
            if ( c == ' ' ) {
              scrapline = 1; // 報錯時要註銷後面
            } // if
            // 讀到空格換行都要驗錯
            cout << "str=" << str << endl;
            Cut( str, 0 ); // 該加進gtokens的加完了
            str = "";
          } // if
        }   // if


        // 是註解的話 這個while照跑但不會做事直到/n
        if ( c == '\n' ) {
          graywords = false;  // 遇到換行 解除註解
        } // if

        c = getchar();
        // cout << "c='" << c << "'" << endl;
        if ( c == ';' )
          scrapline = 1;  // 有報錯要註銷後面
      } // while

      // 讀到;了
      // 把第一個;以前的str略過換行保留空格，放進Check(str);
      cout << "str=" << str << endl;
      Cut( str, 1 );
      Calculate();
    }     // try
    catch ( runtime_error&e ) {
      cout << "> " << e.what() << endl;
      if ( scrapline )
        // 因為空格;所以遇到檢查 所以發現錯誤跳來這的 其實後面還有
        while ( getchar() != '\n' )
          ;
    } // catch
  }     // while 處理每次指令
}     // main

// 3/0?
// quit
