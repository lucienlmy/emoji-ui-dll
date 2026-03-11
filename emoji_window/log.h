#define _CRT_SECURE_NO_WARNINGS
#ifndef LOG_H
#define LOG_H

#include <stdarg.h>
#include <stdio.h>

inline void WriteLog(const char* format, ...) {
    char buffer[1024];
    va_list args;
    va_start(args, format);
    vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    
    // 写到固定路径，便于调试查看
    FILE* f = fopen("C:\\menu_debug.log", "a");
    if (f) {
        fprintf(f, "%s\n", buffer);
        fclose(f);
    }
}

#endif
