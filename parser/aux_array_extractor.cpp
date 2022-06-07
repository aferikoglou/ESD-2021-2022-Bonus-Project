#include <iostream>
#include <clang-c/Index.h>
#include <vector>
using namespace std;

#include <cstring>
int action_point_counter = 1;

ostream& operator<<(ostream& stream, const CXString& str)
{
  stream << clang_getCString(str);
  clang_disposeString(str);
  return stream;
}

// enables analysis only after discovering top level function
void matchTopLevel(int &analysis_flag,CXCursor cc, const char * top_level_func)
{
  if(clang_getCursorKind(cc) == CXCursor_FunctionDecl && analysis_flag == 0)
  {
    const char *fn = clang_getCString(clang_Cursor_getMangling(cc));
    if (strstr(fn,top_level_func) != NULL)
    {
      analysis_flag = 1;
      //cout << fn << endl;
    }
    clang_disposeString(clang_Cursor_getMangling(cc));
  }
}


void print_decl_loc(CXCursor cc)
{
    // this line filters out non-array types
    if (clang_getNumElements(clang_getCursorType(cc)) > 0)
    {
        unsigned line,col;
        CXSourceLocation src = clang_getCursorLocation(cc);
        clang_getExpansionLocation(src,NULL,&line,&col,NULL);
        CXString CXS = clang_getCursorSpelling(cc);
        const char *fn = clang_getCString(CXS);
        cout << "A," <<line - 1<< "," << col - 1 << "," << action_point_counter++ << "," << fn << endl;
        clang_disposeString(CXS);
    }
}

void print_for_loc(CXCursor cc)
{

    unsigned line,col;
    CXSourceLocation src = clang_getCursorLocation(cc);
    clang_getExpansionLocation(src,NULL,&line,&col,NULL);
    cout << "L," <<line - 1<< "," << col - 1 << ","  << action_point_counter++ <<  endl;
}

int analyze = 0;


int main(int argc,char **argv)
{
  CXIndex index = clang_createIndex(0, 0);
  CXTranslationUnit unit = clang_parseTranslationUnit(
    index,
    argv[1], nullptr, 0,
    nullptr, 0,
    CXTranslationUnit_SingleFileParse); //none
  if (unit == nullptr)
  {
    cerr << "Unable to parse translation unit. Quitting." << endl;
    exit(-1);
  }

  CXCursor cursor = clang_getTranslationUnitCursor(unit);
  clang_visitChildren(
    cursor,
    [](CXCursor c, CXCursor parent, CXClientData client_data)
    {      

        if (clang_getCursorKind(c) == CXCursor_VarDecl)
          print_decl_loc(c);
        else if(clang_getCursorKind(c) == CXCursor_ForStmt)
          print_for_loc(c);

      // This begins the analysis of the code when we reach the top-level function and then only.
      //matchTopLevel(analyze,c,"initiate_scan");

      return CXChildVisit_Recurse;
    },
    nullptr);

  clang_disposeTranslationUnit(unit);
  clang_disposeIndex(index);
}