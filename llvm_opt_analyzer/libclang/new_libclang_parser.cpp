#include <iostream>
#include <clang-c/Index.h>
#include <vector>
#include <cstdio>
#include <algorithm>
#include <cstring>
#include <fstream>
#include "new_CursorActions.hpp"
using namespace std;

#define KERNEL_INFO_PRECURSOR "hls_extracted_locs.txt"
#define FNDecls "hls_function_declarations.txt"
// global action point counter for analyzed action points
int ap_counter = 1;
ofstream kernel_info_precursor,fn_decls;

int main(int argc, char **argv)
{
  kernel_info_precursor.open(KERNEL_INFO_PRECURSOR);
  fn_decls.open(FNDecls);

  // ---------------- Open source file for libclang parsing ---------
  // arguments are <source_file> + any number of -I flags for headers
  // CXTranslationUnit_KeepGoing: continue even if errors are found (not really used)
  CXIndex index = clang_createIndex(0, 0);
  CXTranslationUnit unit = clang_parseTranslationUnit(index,argv[1],argv+2,argc-2, nullptr, 0,CXTranslationUnit_None | CXTranslationUnit_KeepGoing);
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
      // Only analyze if code is in the main file (NO code analysis - parsing for headers)
      if (clang_Location_isFromMainFile(clang_getCursorLocation(c)))
      {
          // ----- line, col = location of current cursor in source code (line,column).
          unsigned line,col;
          CXSourceLocation src = clang_getCursorLocation(c);
          clang_getExpansionLocation(src,NULL,&line,&col,NULL);

          /*
          * Switch action based on current Cursor Kind
          * e.g different actions for ForStmt, VarDecl, FuncDecl or anything else needed
          */
          switch (clang_getCursorKind(c))
          {
            case CXCursor_FunctionDecl: FunctionDeclAction(c,line,col,kernel_info_precursor,fn_decls);
              break;

            case CXCursor_CallExpr: CallExprAction(c,line,col,kernel_info_precursor);
              break;

            case CXCursor_ForStmt: ForStmtAction(c,line,col,kernel_info_precursor);
              break;

            case CXCursor_VarDecl: VarDeclAction(c,line,col,kernel_info_precursor);
              break;

            default:
              break;
          }
        }
        return CXChildVisit_Recurse;
    },
    nullptr);

  clang_disposeTranslationUnit(unit);
  clang_disposeIndex(index);
}