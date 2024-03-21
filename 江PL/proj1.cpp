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


string ToStr( Operand a ) {
  ostringstream oss;

  if ( a.Getvartype() == "float" ) {
    oss << a.Getvarvaluef();
    string str( oss.str() );
    return str;
  } // if
  else if ( a.Getvartype() == "int" ) {
    oss << a.Getvarvaluei();
    string str( oss.str() );
    return str;
  } // else if
  else
    return a.Getvarname() + "is not float nor int\n";
} // ToStr()

// 430
// 將一串指定的expression轉後序式 並回傳答案(Operand)
Operand Evaluate( string exp ) {
  Operand ans;

  // 一個數字
  if ( 0 ) {
    ans.Setvalue( exp );
    return ans;
  }

  // 一個IDENT (宣告過)
  if ( 0 ) {
    ans.Setvalue( exp );
    return ans;
  } // if


  // 一段exp算式(含IDENT)

  int mode = 0;

  // 知道ab的值
  if ( a.Getvartype() == "int" && b.Getvartype() == "int" ) {
    int aint = a.Getvarvaluei();
    int bint = b.Getvarvaluei();
  } // if
  else if ( a.Getvartype() == "int" && b.Getvartype() == "float" ) {
    float aflo = a.Getvarvaluei();
    float bflo = b.Getvarvaluef();
    mode = 1;
  }
  else if ( a.Getvartype() == "float" && b.Getvartype() == "int" ) {
    float aflo = a.Getvarvaluef();
    float bflo = b.Getvarvaluei();
    mode = 2;
  }
  else if ( a.Getvartype() == "float" && b.Getvartype() == "float" ) {
    float aflo = a.Getvarvaluef();
    float bflo = b.Getvarvaluef();
    mode = 3;
  }
  else
    cout << "ab are not float or int!";


  if ( op.compare( "+" ) == 0 )
    ;
  else if ( op.compare( "-" ) == 0 )
    ;
  else if ( op.compare( "*" ) == 0 )
    ;
  else if ( op.compare( "/" ) == 0 )
    ;
  else
    ;
  // cout << fixed << setprecision(3) << 3.1234 << endl;
  // cout << ans; //bool/int/float
  return ans;
} // Evaluate()

// 敘述式是否成立
// 可能是float跟int比??
bool IsItTrue( Operand a, Operand b, string cmp_op ) {
  // 左右都已經算出一個Operand值了，簡單比大小就好
  if ( a.Getvartype() == "int" ) int A = a.Getvarvaluei();
  else if ( a.Getvartype() == "float" ) float A = a.Getvarvaluef();

  if ( b.Getvartype() == "int" ) int B = b.Getvarvaluei();
  else if ( b.Getvartype() == "float" ) float B = b.Getvarvaluef();

  if ( cmp_op.compare( "<" ) == 0 )
    return A < B;
  else if ( cmp_op.compare( "<=" ) == 0 )
    return A <= B;
  else if ( cmp_op.compare( ">" ) == 0 )
    return A > B;
  else if ( cmp_op.compare( ">=" ) == 0 )
    return A >= B;
  else if ( cmp_op.compare( "<>" ) == 0 )
    return A != B;
  else if ( cmp_op.compare( "=" ) == 0 )
    return A == B;
} // IsItTrue()

// Operand 轉string? (True/False直接印就好了)
void Printans( Operand ans ) {
} // Printans()

bool Check( Token a, Token b );


void Cut( string str, bool isend ) {
  if ( str.compare( "" ) == 0 )
    return;

  int apair = 0;
  // 遍歷整個str檢測第一型錯誤(一次一個字元)
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
        throw runtime_error( "Unexpected token : ')'" );
    } // if
    else if ( i < str.size() - 1 && str.substr( i, 2 ) == ":=" ) { // :不是最後一個且後面是=
      // 合法
      i++;                                                  // 因為一次看兩個字所以要i++
    } // else if
    else                                                    // 不合法
      // 遞迴錯誤字元以前的東西????
      throw runtime_error( "Unrecognized token with first char : '" + str.substr( i, 1 ) + "'" );
    // else
  } // for

  if ( apair != 0 )
    throw runtime_error( "Unrecognized token with first char : ';(((('" );

  Token tokens[ 1000 ];
  int   tokens_size = 0;
  bool  assign      = 0;

  // 切token + 檢測第二型錯誤(文意)(一次多個字元為一個token)
  // 跳過空格??
  for ( int i = 0 ; i < str.size() ;) {
    if ( str.substr( i, 1 ) == " " )
      i++;
    // 2
    else if ( str.substr( i, 2 ) == "<=" || str.substr( i, 2 ) == ">=" ||
              str.substr( i, 2 ) == "<>" || str.substr( i, 2 ) == ":=" ) {
      if ( assign && str.substr( i, 2 ) == ":=" )
        throw runtime_error( "Unexpected token : ':='" );
      if ( str.substr( i, 2 ) == ":=" )
        // assign符號很特殊不能出現兩次所以文法上要特別處理
        assign = 1;

      Token tk( str.substr( i, 2 ) );
      tokens[ tokens_size ] = tk;
      tokens_size++;
      i += 2;
    } // else if
    // 1
    else if ( str.substr( i, 1 ) == "<" || str.substr( i, 1 ) == ">" || str.substr( i, 1 ) == "+" ||
              str.substr( i, 1 ) == "-" || str.substr( i, 1 ) == "*" || str.substr( i, 1 ) == "/" ||
              str.substr( i, 1 ) == "(" || str.substr( i, 1 ) == ")" || str.substr( i, 1 ) == "=" ) {
      // +-*/=()><
      Token tk( str.substr( i, 1 ) );
      tokens[ tokens_size ] = tk;
      if ( tokens_size == 0 && ( str.substr( i, 1 ) == "+" || str.substr( i, 1 ) == "-" ) )
        tokens[ tokens_size ].Modifytype( "sign" );
      if ( ( tokens_size > 0 ) && ( str.substr( i, 1 ) == "+" || str.substr( i, 1 ) == "-" ) &&
           ( tokens[ tokens_size - 1 ].Gettype() == "arith" || tokens[ tokens_size - 1 ].Gettype() == "left" ||
             tokens[ tokens_size - 1 ].Gettype() == "assign" ||
             tokens[ tokens_size - 1 ].Gettype() == "boolean_opt" ) )
        tokens[ tokens_size ].Modifytype( "sign" );
      tokens_size++;
      i++;
    } // else if
    // 數字小數點
    else if ( ( str[ i ] >= '0' && str[ i ] <= '9' ) || str[ i ] == '.' ) {
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
        throw runtime_error( "Unexpected token : '" + wrong + "'" );
      if ( number == "." )
        throw runtime_error( "Unrecognized token with first char : '.'" );
      Token tk( number );
      tokens[ tokens_size ] = tk;
      tokens_size++;
    } // else if
    // AZ_az
    else if ( str[ i ] == '_' )
      throw runtime_error( "Unrecognized token with first char : '_'" );
    else if ( ( str[ i ] >= 'a' && str[ i ] <= 'z' ) || ( str[ i ] >= 'A' && str[ i ] <= 'Z' ) ) {
      string variable;
      variable += str[ i ];
      i++;
      while ( ( str[ i ] >= 'a' && str[ i ] <= 'z' ) || ( str[ i ] >= 'A' && str[ i ] <= 'Z' ) ||
              str[ i ] == '_' || ( str[ i ] >= '0' && str[ i ] <= '9' ) ) {
        variable += str[ i ];
        i++;
      } // while
      Token tk( variable );
      tokens[ tokens_size ] = tk;
      tokens_size++;
    } // else if
  }   // for

  // 丟進check做前後文法檢查
  for ( int i = 0 ; i < tokens_size - 1 ; i++ )
    if ( ! Check( tokens[ i ], tokens[ i + 1 ] ) )
      throw runtime_error( "Unexpected token : '" + tokens[ i + 1 ].Getdata() + "'" );

  // 這次丟進來檢查是因為分號的話
  if ( isend ) {
    // cout << "check because ';'\n";
    // cout << tokens[tokens_size - 1].Gettype();
    cout << tokens[ tokens_size - 1 ].Gettype();
    cout << tokens[ tokens_size - 1 ].Getdata();
    if ( ! ( tokens[ tokens_size ].Gettype() == "num" || tokens[ tokens_size ].Gettype() == "IDENT" ||
             tokens[ tokens_size ].Gettype() == "right" ) ) {
      cout << "\nwrong!!\n";
      throw runtime_error( "Unexpected token : ';'" );     // !!!!!!!!!!!!!!!
    } // if
  } // if

  cout << str << ":correct\n";


  // ------------------------------------------------------------------------------------------------
  // 以下開始calculate
  // 若不是end就不用走下去
  // 為了不宣告全域變數所以calculate寫在Cut()裡
  if ( isend ) {
    Operand operands[ 1000 ]; // 存被乘數和宣告過的operand之類的
    int     numOfoperands = 0;

    int sentence = -1; // 定義式0 判斷式1 計算式-1

    // 判斷這是一個甚麼式 by"檢查有無cmp_op和:="
    for ( int i = 0 ; i <= tokens_size - 1 && sentence == -1 ; i++ ) {
      // 但凡讀到未宣告過的IDENT直接報錯
      if ( tokens[ i ].Gettype() == "IDENT" && tokens[ i + 1 ].Getdata() != ":=" ) {
        string newvar = tokens[ i ].Getdata();
        bool   find   = 0;
        for ( int j = 0 ; j < numOfoperands && ! find ; j++ )
          if ( operands[ numOfoperands ].Getvarname().compare( newvar ) == 0 )
            find = 1;

        if ( ! find )
          throw runtime_error( "Undefided identifier : '" + newvar + "'" );
      } // if


      // 讀到:=就是定義式
      if ( tokens[ i ].Getdata() == ":=" ) {
        sentence = 0;
        // 等號左邊的是名子
        string varname = tokens[ i - 1 ].Getdata();
        // 等號右邊(直到分號為止都是exp)(若不是exp就throw)丟進Evaluate()會回傳一個Operand
        string exp = "";
        for ( int j = i + 1 ; j < tokens_size ; j++ ) {
          if ( tokens[ j ].Gettype() == "num" || tokens[ j ].Gettype() == "left" ||
               tokens[ j ].Gettype() == "right" || tokens[ j ].Gettype() == "IDENT" ||
               tokens[ j ].Gettype() == "arith" || tokens[ j ].Gettype() == "sign" ) {
            // 剩餘exp還是有可能讀到沒見過的
            if ( tokens[ j ].Gettype() == "IDENT" ) {
              string newvar = tokens[ j ].Getdata();
              bool   find   = 0;
              for ( int k = 0 ; k < numOfoperands && ! find ; k++ )
                if ( operands[ numOfoperands ].Getvarname().compare( newvar ) == 0 )
                  find = 1;

              if ( ! find )
                throw runtime_error( "Undefided identifier : '" + newvar + "'" );
            } // if
            exp += tokens[ j ].Getdata();
          }   // if
          else   // 如果後面有東西使其不是一個exp(> < >= <= <> = :=)
            throw runtime_error( "Unexpected token : '" + tokens[ j ].Getdata() + "'" );
          // else
        } // for
        Operand var( varname, ToStr( Evaluate( exp ) ) ); // 型別： string, string
        // 新增一格Operand
        operands[ numOfoperands ] = var;
        numOfoperands++;
        i = tokens_size; // 不用讀了 下一則指令謝謝
      } // if


      // 讀到boolean_opt就是敘述式
      if ( tokens[ i ].Gettype() == "boolean_opt" )
        sentence = 1;
      // if
    }               // for(判斷完成)

    // 這是定義式
    if ( sentence == 0 ) {
      // 做完就可以離開Cut()了吧
    }
    // 這是敘述式203
    if ( sentence == 1 ) {
      // boolean_opt左右都要重讀
      // 直到分號為止都是exp)(若不是exp就throw)丟進Evaluate()會回傳一個Operand
      // IsItTrue()會回傳一個bool
      string exp = "";
      for ( int j = i + 1 ; j < tokens_size ; j++ ) {
        if ( tokens[ j ].Gettype() == "num" || tokens[ j ].Gettype() == "left" ||
             tokens[ j ].Gettype() == "right" || tokens[ j ].Gettype() == "IDENT" ||
             tokens[ j ].Gettype() == "arith" || tokens[ j ].Gettype() == "sign" ) {
          // 剩餘exp還是有可能讀到沒見過的
          if ( tokens[ j ].Gettype() == "IDENT" ) {
            string newvar = tokens[ j ].Getdata();
            bool   find   = 0;
            for ( int k = 0 ; k < numOfoperands && ! find ; k++ )
              if ( operands[ numOfoperands ].Getvarname().compare( newvar ) == 0 )
                find = 1;

            if ( ! find )
              throw runtime_error( "Undefided identifier : '" + newvar + "'" );
          }       // if
          exp += tokens[ j ].Getdata();
        }         // if
        else      // 如果後面有東西使其不是一個exp(> < >= <= <> = :=)
          throw runtime_error( "Unexpected token : '" + tokens[ j ].Getdata() + "'" );
      }           // for
      string rightval = ToStr( Evaluate( exp ) );
      IsItTrue(); // 203
      // 拿著token資料建立Operand丟進IsItTrue()
      // cout << IsItTrue(Operand a, Operand b, char cmp_op);
    }
    // 計算式152
    else if ( sentence == -1 ) {
      // 整串丟進Evaluate()得出一個Operand
      // Printans(Evaluate(exp));
    }
  } // if(isend) do the Evaluate()


  // throw runtime_error("Unexpected token : '" + str.substr(0, 1) + "'");
  // semantic error(Undefided identifier)變數未宣告
  // throw runtime_error("Undefided identifier : '" + str.substr(0, 1) + "'");
} // Cut()

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
       ( b.Gettype() == "arith" || b.Gettype() == "boolean_opt" || b.Gettype() == "right" ) )
    return 1;

  if ( a.Gettype() == "boolean_opt" &&
       ( b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num" ) )
    return 1;

  if ( a.Gettype() == "arith" &&
       ( b.Gettype() == "sign" || b.Gettype() == "left" || b.Gettype() == "num" || b.Gettype() == "IDENT" ) )
    return 1;

  return 0;
}

int main() {
  // getchar()

  string utestnum;

  cin >> utestnum;
  if ( utestnum == "quit" ) {
    cout << "Program exits...because utestnum\n";
    return 0;
  }
  cout << "Program starts...\n";
  getchar();


  bool scrapline = 0;

  while ( 1 ) {
    scrapline = 0;
    try{
      string str            = "";
      char   c              = ' ';
      bool   alreadyHasADiv = 0;
      bool   graywords      = 0;
      c = getchar(); // 獨到前一行最後的enter
      while ( c != ';' ) {
        if ( str == "quit" ) {
          cout << "Program exits...";
          return 0;
        }
        if ( ! graywords ) {
          if ( c == '/' ) {
            if ( alreadyHasADiv ) {
              graywords = 1;
              // alreadyHasADiv = 0;
            }
            else
              alreadyHasADiv = 1;
          }
          else if ( alreadyHasADiv ) {
            alreadyHasADiv = 0;
            // 在這裡才知道前一個是除不是註解 所以現在才加前一個(/)進str
            str += '/';
          }

          if ( c != ' ' && c != '\n' && c != '\t' && c != '/' ) // 加本人
            str += c;
          if ( c == '\n' || c == ' ' ) {
            str += ' ';
            if ( c == ' ' )
              scrapline = 1;
            // cout << "check" << str << " ";
            Cut( str, 0 ); // function裡有1000格token
            // 沒分號直接按enter的話還是要檢測文法錯
            // 如果檢測發現是錯的就會跳走但後面再錯都不要理
          }
        } // if
        if ( c == '\n' ) {
          graywords = false;
          // 註解域到換行 解除註解
        }
        c = getchar();
        if ( c == ';' )
          scrapline = 1;
      } // while
        // 把第一個;以前的str略過註解和換行保留空格，放進Check(str);
      if ( str == "quit" ) {
        cout << "Program exits....\n";
        return 0;
      }
      Cut( str, 1 );
      // Evaluate();
    }     // try
    catch ( runtime_error&e ) {
      cout << "> " << e.what() << endl;
      if ( scrapline )
        // 因為空格;所以遇到檢查 所以發現錯誤跳來這的 其實後面還有
        while ( getchar() != '\n' )
          ;
    } // catch
  }     // while 處理每次指令
}         // main

// 3/0?
// quit











