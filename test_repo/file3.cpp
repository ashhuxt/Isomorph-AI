#include <vector>
int sum_list(const std::vector<int>& data) {
    int s = 0;
    for (int x : data) {
        s += x;
    }
    return s;
}
