# virtual_machine  
 가상의 virtual machine을 구현해 과제를 위해 생성한 petite language를 해석하여 특정 기능을 수행할 수 있는 machine  
 명령어    
 1) LABEL:  
    현재 위치를 LABEL이라는 이름으로 정의  
    LABEL의 라벨과 줄번호를 메모리에 저장   
    (ex) 'HERE:', 'LOOP:', 'SNU:' 등등  
 2) jmp E, LABEL  
    E의 값이 0이 아니라면, LABEL로 가서 실행  
    E의 값이 0이라면 바로 다음줄 실행  
    E가 숫자가 아니라면 Illegal Value  
    LABEL이 이미 정의된 LABEL이 아니라면 Unknown LABEL  
 3) print(E)  
    E를 출력 : 정수, list 모두 가능  
 4) x = E // E는 정수  
 5) x = [E1; E2] : E1이 E2개 연속되어 있는 리스트를 x에 저장  
 6) x[E1] = E2 : x list의 E1번 째 원소가 E2로 설정  
 7) 표현식  
    (E) : 우선순위를 갖는 E  
    E1 op E2 : operator(+,-,/,*,==,!=,<=,>=,>,<)
    input() : 키보드로 정수 입력받기
 8) 파일 설명
     __init__  
    exceptions : 예외 상황들 받아서 처리  
    ixx : 길이가 고정된 2진수 정수에 대한 처리 함수  
    petite_vm: virtual machine 구현  
    utils: in2post 구현  
    virtual_machine:  
    exceptions: 예외 처리 함수, 예외 처리는 전부 구현되지는 않음  
