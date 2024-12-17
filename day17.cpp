
#include <list>
#include <iostream>
#include <iterator>
#include <fstream>
#include <cmath>
#include <string>

using namespace std;

class AOC3
{
public:
    int reg_a, reg_b, reg_c;
    int head;
    char *program;
    int program_length;

    std::list<int> output;

    AOC3()
    {
        reg_a = 0;
        reg_b = 0;
        reg_c = 0;

        head = 0;
        output = std::list<int>();
    }

    void load_program(char *program, int length)
    {
        this->program = program;
        this->head = 0;
    }

    void execute()
    {
        while (head < program_length)
        {
            char op = program[head];
            int val = program[head + 1];
            switch (op)
            {
            case 0:
                adv(val);
                break;
            case 1:
                bxl(val);
                break;
            case 2:
                bst(val);
                break;
            case 3:
                jnz(val);
                break;
            case 4:
                bxc(val);
                break;
            case 5:
                out(val);
                break;
            case 6:
                bdv(val);
                break;
            case 7:
                cdv(val);
                break;
            default:
                cout << "Unknown op code " << op << endl;
                break;
            }
            head += 2;
        }
    }

    void reset()
    {
        reg_a = 0;
        reg_b = 0;
        reg_c = 0;
        head = 0;
        output.clear();
    }

    void print_output()
    {
        for (int o : output)
        {
            std::cout << o << ",";
        }
        std::cout << "END" << endl;
    }

    int combo(int val)
    {
        switch (val)
        {
        case 0:
            return 0;
        case 1:
            return 1;
        case 2:
            return 2;
        case 3:
            return 3;
        case 4:
            return reg_a;
        case 5:
            return reg_b;
        case 6:
            return reg_c;
        default:
            return 0;
        }
    }

    void adv(int val)
    {
        reg_a = reg_a / (std::pow(2, combo(val)));
    }

    void bxl(int val)
    {
        reg_b = val ^ reg_b;
    }

    void bst(int val)
    {
        reg_b = combo(val) % 8;
    }

    void jnz(int val)
    {
        if (reg_a != 0)
        {
            head = val - 2;
        }
    }

    void bxc(int val)
    {
        reg_b = reg_b ^ reg_c;
    }

    void out(int val)
    {
        output.push_back(combo(val) % 8);
        // cout << combo(val)%8 << ",";
    }

    void bdv(int val)
    {
        reg_b = reg_a / (std::pow(2, combo(val)));
    }

    void cdv(int val)
    {
        reg_c = reg_a / (std::pow(2, combo(val)));
    }

    // This is why everyone hates you, C++
    /*AOC3* read_from_file(string filename){
        AOC3* aoc3 = new AOC3();
        string line;

        std::ifstream infile(filename);

        if (!infile.is_open()) {
            std::cerr << "Error: Unable to open the file." << std::endl;
            return nullptr;
        }
        std::istream_iterator<std::string> it(infile);
        std::istream_iterator<std::string> end;

        if (it == end) {
            std::cerr << "Error: Empty file." << std::endl;
            return nullptr;
        }

        while (it != end) {
            string line = *it++;
            if (line.find("Register A: ") >= 0) {

            }
                aoc3.reg_a = int(line.split(":")[1])
            if line.startswith("Register B: "):
                aoc3.reg_b = int(line.split(":")[1])
            if line.startswith("Register C: "):
                aoc3.reg_c = int(line.split(":")[1])
            if line.startswith("Program"):
                ops = line.split(":")[1]
                ops = list([int(o) for o in ops.split(",")])
                aoc3.load_program(ops)
        }
        cout << s.substr(last) << endl;
        while ((pos = in_str.find("\n")) != std::string::npos) {
            std::string line =
        return aoc3
    }*/
};

int main()
{
    cout << "Welcome to the AoC3 Computer..." << endl;
    AOC3 computer = AOC3();
    char prog[] = {2,4,1,5,7,5,1,6,4,1,5,5,0,3,3,0};
    int l = 16;
    computer.program = prog;
    computer.program_length = l;
    computer.reg_a = 60589763;
    computer.execute();
    computer.print_output();

    int a = 601100000;
    bool found = false;
    while (!found) {
        a += 1;
        computer.reset();
        computer.reg_a = a;
        computer.execute();

        auto it = computer.output.begin();
        found = true;
        for(int i = 0; i < computer.program_length; i++) {
            // cout << to_string(prog[i]) << ", " << *it << ";";
            if(computer.program[i] != *it++) {
                found = false;
            }
        }
        if(it != computer.output.end())
            found = false;
        if (a % 100000 == 0)
            cout << "Iteration " << a << endl;
    }

    cout << "Program results in itself at Iteration " << a << endl;

    cout << "Computation finished. Goodbye!" << endl;
    return 0;
}
