
#include <iostream>
#include <string>


int main(int argc, const char* argv[]){

    std::cout<< "This programme is used for tests the instrumentation of the programme with the three tools" << std::endl;

    
    std::string precision{ argv[1] };
    std::string mode{ argv[3] };
    std::string operation{ argv[2] };
    int nbr_loop = std::stoi(argv[4]);
    float a = std::stof(argv[5]);
    float b = std::stof(argv[6]);
    float acc = a;


    if(operation.compare("add")==0){
        for(int i = 0; i < nbr_loop; i++){
            acc = acc + b;
        }
    }
    if(operation.compare("sub")==0){
        for(int i = 0; i < nbr_loop; i++){
            acc = acc - b;
        }
    }
    if(operation.compare("mul")==0){
        for(int i = 0; i < nbr_loop; i++){
            acc = acc * b;
        }
    }

    std::cout << "Result : " << acc << std::endl;

    return 0;
}