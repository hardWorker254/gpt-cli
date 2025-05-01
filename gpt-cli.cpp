#ifdef _WIN32
    #include <windows.h>
#else
    #include <cstdlib>
    #include <unistd.h>
#endif

using namespace std;

int main() {
    system("python /usr/local/bin/gpt-clil/main.py");
    return 0;
}