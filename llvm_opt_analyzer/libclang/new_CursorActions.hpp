#include <iostream>
#include <clang-c/Index.h>
#include <fstream>
#include <cassert>
#include <vector>
#include <algorithm>
using namespace std;

/*
* New parser file: Much of the functionality found here has been moved to LLVM + Opt
* This is a simplified version and removes the need for code compilation and heuristics that can fail in many situations
*/

// operator overload for printing CXString
ostream& operator<<(ostream& stream, const CXString& str)
{
  stream << clang_getCString(str);
  clang_disposeString(str);
  return stream;
}

extern int ap_counter;

void ForStmtAction(CXCursor c,unsigned line, unsigned col, ofstream &kernel_precursor)
{
    assert(clang_getCursorKind(c) == CXCursor_ForStmt);
    kernel_precursor << "L," <<line - 1<< "," << col - 1 << ","  << ap_counter++ <<  endl;
}

// variable loop_ranges unused, only included to maintain conformity with other similar functions
void VarDeclAction(CXCursor c,unsigned line, unsigned col, ofstream &kernel_precursor)
{
    assert(clang_getCursorKind(c) == CXCursor_VarDecl);
    if  (clang_getNumElements(clang_getCursorType(c)) <= 0) // > 0 only for array like objects
        return;

    CXString CXS = clang_getCursorSpelling(c);
    const char *fn = clang_getCString(CXS);
    kernel_precursor << "A," <<line - 1<< "," << col - 1 << "," << ap_counter++ << "," << fn << endl;
    clang_disposeString(CXS);  
}

// variable kernel_precursor unused, only included to maintain conformity with other similar functions
void FunctionDeclAction(CXCursor c,unsigned line, unsigned col, ofstream &kernel_precursor, ofstream &fn_decls)
{
    assert(clang_getCursorKind(c) == CXCursor_FunctionDecl);
    CXSourceRange range = clang_getCursorExtent(c);
    CXSourceLocation start = clang_getRangeStart(range), end = clang_getRangeEnd(range);
    unsigned lstart,lend;
    clang_getExpansionLocation(start,NULL,&lstart,NULL,NULL);
    clang_getExpansionLocation(end,NULL,&lend,NULL,NULL);
    // FND: FuNction Declaration
    fn_decls << clang_getCursorSpelling(c) << "," << lstart << "," << lend << endl; 
}

void CallExprAction(CXCursor c,unsigned line, unsigned col, ofstream &kernel_precursor)
{
    assert(clang_getCursorKind(c) == CXCursor_CallExpr);
    /*CXString s = clang_getCursorSpelling(c);
    const char *str = clang_getCString(s);
    // FNC: FuNction Call
    if (str[0] != '\0') // this catches some strange things such as casts etc.
        loop_ranges << "FNC:" << ","<< str << line << "," << col << endl;
    clang_disposeString(s);*/
}