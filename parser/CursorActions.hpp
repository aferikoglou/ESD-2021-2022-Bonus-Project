#include <iostream>
#include <clang-c/Index.h>
#include <fstream>
#include <cassert>
#include <vector>
#include <algorithm>
using namespace std;

// operator overload for printing CXString
ostream& operator<<(ostream& stream, const CXString& str)
{
  stream << clang_getCString(str);
  clang_disposeString(str);
  return stream;
}

// checks if a line is in the exclusion list
int exclude_line(const vector<int> &v,int cl){return binary_search(v.begin(),v.end(),cl);}

// ap_counter defined in main file
extern int ap_counter;
// ap_invisible_counter defined in main file
extern int ap_invisible_counter;

void ForStmtAction(CXCursor c,unsigned line, unsigned col, const vector<int> &exclusion_list, ofstream &kernel_precursor, ofstream &loop_ranges)
{
    assert(clang_getCursorKind(c) == CXCursor_ForStmt);

    if (exclude_line(exclusion_list,line) == false)
        kernel_precursor << "L," <<line - 1<< "," << col - 1 << ","  << ap_counter <<  endl;
    // range: the part ot the source code that the loop covers
    CXSourceRange range = clang_getCursorExtent(c);
    CXSourceLocation start = clang_getRangeStart(range), end = clang_getRangeEnd(range);
    // line_start: line in which the loop starts
    // line_end: line in which the loop ends
    // same for column_start,column_end
    unsigned line_start,line_end,column_start,column_end;
    clang_getExpansionLocation(start,NULL,&line_start,&column_start,NULL);
    clang_getExpansionLocation(end,NULL,&line_end,&column_end,NULL);

    if (exclude_line(exclusion_list,line) == false)
        loop_ranges << "L" << ap_counter++ << ":"<< line_start << "," << column_start << "," << line_end << "," << column_end << endl;
    else
        loop_ranges << "I" << ap_invisible_counter++ << ":"<< line_start << "," << column_start << "," << line_end << "," << column_end << endl;

    return;
}

// variable loop_ranges unused, only included to maintain conformity with other similar functions
void VarDeclAction(CXCursor c,unsigned line, unsigned col, const vector<int> &exclusion_list, ofstream &kernel_precursor,ofstream &loop_ranges)
{
    assert(clang_getCursorKind(c) == CXCursor_VarDecl);
    if  (clang_getNumElements(clang_getCursorType(c)) <= 0) // > 0 only for array like objects
        return;

    CXString CXS = clang_getCursorSpelling(c);
    const char *fn = clang_getCString(CXS);
    kernel_precursor << "A," <<line - 1<< "," << col - 1 << "," << ap_counter++ << "," << fn << endl;
    clang_disposeString(CXS);
    return;
}

// variable kernel_precursor unused, only included to maintain conformity with other similar functions
void FunctionDeclAction(CXCursor c,unsigned line, unsigned col, const vector<int> &exclusion_list, ofstream &kernel_precursor,ofstream &loop_ranges)
{
    assert(clang_getCursorKind(c) == CXCursor_FunctionDecl);
    // FND: FuNction Declaration
    loop_ranges << "FND:" << clang_getCursorSpelling(c) << endl;
    return;
}

void CallExprAction(CXCursor c,unsigned line, unsigned col, const vector<int> &exclusion_list, ofstream &kernel_precursor,ofstream &loop_ranges)
{
    assert(clang_getCursorKind(c) == CXCursor_CallExpr);
    CXString s = clang_getCursorSpelling(c);
    const char *str = clang_getCString(s);
    // FNC: FuNction Call
    if (str[0] != '\0') // this catches some strange things such as casts etc.
        loop_ranges << "FNC:" << ","<< str << line << "," << col << endl;
    clang_disposeString(s);
    return;
}