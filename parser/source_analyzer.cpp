#include <iostream>
#include <clang-c/Index.h>
#include <vector>
using namespace std;

#include <cstring>

struct FunctionCalls
{
    CXString curFunctionName;
    vector<CXString> offsprings;
};

ostream& operator<<(ostream& stream, const CXString& str)
{
  stream << clang_getCString(str);
  clang_disposeString(str);
  return stream;
}


vector<FunctionCalls> f_calls;
FunctionCalls current_f_call;

int ap_counter = 1;

int main(int argc, char **argv)
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
            unsigned line,col;
            CXSourceLocation src = clang_getCursorLocation(c);
            clang_getExpansionLocation(src,NULL,&line,&col,NULL);
            if (clang_getCursorKind(c) == CXCursor_FunctionDecl)
            {
                cout << "FND:" << clang_getCursorSpelling(c) << endl;
            }
            else if (clang_getCursorKind(c) == CXCursor_CallExpr)
            {
                CXString s = clang_getCursorSpelling(c);
                const char *str = clang_getCString(s);
                if (str[0] != '\0')
                    cout << "FNC:" << ","<< str << line << "," << col << endl;
                clang_disposeString(s);
            }
            else if (clang_getCursorKind(c) == CXCursor_ForStmt)
            {
                CXSourceRange range = clang_getCursorExtent(c);
                CXSourceLocation start = clang_getRangeStart(range), end = clang_getRangeEnd(range);
                unsigned line_start,line_end,column_start,column_end;
                clang_getExpansionLocation(start,NULL,&line_start,&column_start,NULL);
                clang_getExpansionLocation(end,NULL,&line_end,&column_end,NULL);

                cout << "L" << ap_counter++ << ":"<< line_start << "," << column_start << "," << line_end << "," << column_end << endl;

            }
            else if (clang_getCursorKind(c) == CXCursor_VarDecl)
              ap_counter++;

            return CXChildVisit_Recurse;
        }
        return CXChildVisit_Recurse;
    },
    nullptr);

  clang_disposeTranslationUnit(unit);
  clang_disposeIndex(index);
}