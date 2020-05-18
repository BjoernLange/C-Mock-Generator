#ifndef __UNDER_TEST_H__
#define __UNDER_TEST_H__

int do_something_fixed_size(int i);

int do_something_null_terminated(char first, char second);

int do_something_null_terminated_twice(char first, int second);

int do_something_length_described(int first, int second);

int do_something_utf8(wchar_t first, wchar_t second);

#endif