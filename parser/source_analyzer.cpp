#include <iostream>
#include <clang-c/Index.h>
#include <vector>
#include <cstdio>
#include <algorithm>
using namespace std;


#define HLS_EXCLUSION_FILE "hls_exclusion_list.txt"

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

int exclude_line(const vector<int> &v,int cl)
{
  return binary_search(v.begin(),v.end(),cl);
}


vector<FunctionCalls> f_calls;
FunctionCalls current_f_call;

int ap_counter = 1;
vector<int> exclusion_list;

int main(int argc, char **argv)
{

  FILE *f_in = fopen(HLS_EXCLUSION_FILE,"r");
  int exclusion_points = 0,ep;
  if (f_in != NULL)
  {
    fscanf(f_in,"%i",&exclusion_points);
    for (int i = 0;i<exclusion_points;i++)
    {
      fscanf(f_in,"%i",&ep);
      exclusion_list.push_back(ep);
    }
  }
  else
  {
    cout << "--- Error: failed to open HLS exclusion file, aborting" << endl;
    return 1;
  }
  fclose(f_in);



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

            if (exclude_line(exclusion_list,line) == false)
            {
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
              else if (clang_getCursorKind(c) == CXCursor_VarDecl && clang_getNumElements(clang_getCursorType(c)) > 0)
              {
                ap_counter++;
              }
            }
            

            return CXChildVisit_Recurse;
        }
        return CXChildVisit_Recurse;
    },
    nullptr);

  clang_disposeTranslationUnit(unit);
  clang_disposeIndex(index);
}