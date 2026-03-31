#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <stdio.h>

HMODULE g_emoji_window_module = nullptr;

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH: {
        g_emoji_window_module = hModule;
        FILE* f = fopen("C:\\menu_debug.log", "w");
        if (f) {
            fprintf(f, "DLL_PROCESS_ATTACH: hModule=%p\n", hModule);
            fclose(f);
        }
        break;
    }
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        if (ul_reason_for_call == DLL_PROCESS_DETACH) {
            g_emoji_window_module = nullptr;
        }
        break;
    }
    return TRUE;
}
