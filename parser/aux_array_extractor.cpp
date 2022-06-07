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

void print_decl_loc(CXCursor cc)
{
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
    argv[1],argv+2,argc-2,
    nullptr, 0,
    CXTranslationUnit_None | CXTranslationUnit_KeepGoing); //none
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
      if (clang_Location_isFromMainFile(clang_getCursorLocation(c)))
      {
        if (clang_getCursorKind(c) == CXCursor_VarDecl)
          print_decl_loc(c);
        else if(clang_getCursorKind(c) == CXCursor_ForStmt)
          print_for_loc(c);


       /* unsigned line,col;
        CXSourceLocation src = clang_getCursorLocation(c);
        clang_getExpansionLocation(src,NULL,&line,&col,NULL);
        cout << line << " Cursor '" << clang_getCursorSpelling(c) << "' of kind '"
        << clang_getCursorKindSpelling(clang_getCursorKind(c)) << "'\n";*/
        
        return CXChildVisit_Recurse;
      }
      return CXChildVisit_Recurse;
    },
    nullptr);

  clang_disposeTranslationUnit(unit);
  clang_disposeIndex(index);
}