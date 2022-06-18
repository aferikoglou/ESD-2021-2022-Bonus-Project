#include <iostream>
#include <clang-c/Index.h>
#include <vector>
#include <cstdio>
#include <algorithm>
#include <cstring>
#include <fstream>

#include "CursorActions.hpp"

using namespace std;

#define HLS_EXCLUSION_FILE "hls_exclusion_list.txt"
#define KERNEL_INFO_PRECURSOR "hls_extracted_locs.txt"
#define LOOP_RANGES_FILE "hls_loop_ranges.txt"


// global action point counter for analyzed action points
int ap_counter = 1;
// global action point counter for ignored action points
int ap_invisible_counter = 1;

ofstream kernel_info_precursor, loop_ranges_file;

// lines contained in "exclusion list" will NOT be analyzed - optimized
vector<int> exclusion_list;

int main(int argc, char **argv)
{
  FILE *f_in;


  kernel_info_precursor.open(KERNEL_INFO_PRECURSOR);
  loop_ranges_file.open(LOOP_RANGES_FILE);

  int exclusion_points = 0,ep;

  // --------------- Create Exclusion List -----------------

  f_in = fopen(HLS_EXCLUSION_FILE,"r");
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
            case CXCursor_FunctionDecl: FunctionDeclAction(c,line,col,exclusion_list,kernel_info_precursor,loop_ranges_file);
              break;

            case CXCursor_CallExpr: CallExprAction(c,line,col,exclusion_list,kernel_info_precursor,loop_ranges_file);
              break;

            case CXCursor_ForStmt: ForStmtAction(c,line,col,exclusion_list,kernel_info_precursor,loop_ranges_file);
              break;

            case CXCursor_VarDecl: VarDeclAction(c,line,col,exclusion_list,kernel_info_precursor,loop_ranges_file);
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