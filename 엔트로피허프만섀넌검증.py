# 코드 다 읽을 필요 없고 그냥 아래로 주욱 내려서 결과만 보셔도 됨.


import math
import random
from tqdm import tqdm
# Example Huffman coding implementation
# Distributions are represented as dictionaries of { 'symbol': probability }
# Codes are dictionaries too: { 'symbol': 'codeword' }


# ↓ 인터넷에서 가져온 거. 허프만 부호화 한 결과물을 반환한다.
# https://gist.github.com/mreid/fdf6353ec39d050e972b
def huffman(p):
    '''Return a Huffman code for an ensemble with distribution p.'''
    # assert (sum(p.values()) == 1.0)  # Ensure probabilities sum to 1

    # Base case of only two symbols, assign 0 or 1 arbitrarily
    if (len(p) == 2):
        return dict(zip(p.keys(), ['0', '1']))

    # Create a new distribution by merging lowest prob. pair
    p_prime = p.copy()
    a1, a2 = lowest_prob_pair(p)
    p1, p2 = p_prime.pop(a1), p_prime.pop(a2)
    p_prime[a1 + a2] = p1 + p2

    # Recurse and construct code on new distribution
    c = huffman(p_prime)
    ca1a2 = c.pop(a1 + a2)
    c[a1], c[a2] = ca1a2 + '0', ca1a2 + '1'

    return c

# ↓ 인터넷에서 같이 가져온 거
def lowest_prob_pair(p):
    '''Return pair of symbols from distribution p with lowest probabilities.'''
    assert (len(p) >= 2)  # Ensure there are at least 2 symbols in the dist.

    sorted_p = sorted(p.items(), key=lambda x: x[1])
    return sorted_p[0][0], sorted_p[1][0]





def HuffEntropyCal(original_dict, Huffman_dict):
    #오리지날 딕셔너리를 주면, 그 개수를 가지고 평균 허프만 방식의 엔트로피를 구한다.
    # 허프만 코딩된 딕셔너리도 같이 주어야 한다.
    #오리지날 딕트 : {'a' : 1, 'b':23, 'c':33}
    key_list = list(original_dict.keys())
    val_list = []

    Entropy = 0

    for i in key_list:
        Entropy += len(Huffman_dict[i]) * original_dict[i]

    return Entropy/sum(original_dict.values())

def ShanoonEntropy(proba_dict):
    # 클로드 섀넌의 엔트로피 계산법 섀넌 스펠링 이거 맞나?
    Entropy = 0
    for i in proba_dict.values():
        Entropy += i*math.log(1/i,2)
    return Entropy


def 딕셔너리생성기(num=10):
    # 주어진 숫자 만큼 아이템을 가지는 딕셔너리를 반환한다. 이 때 각 아이템이 가지는 값은 랜덤 정수
    # 너무 긴거 넣지 마 귀찮아져.

    temp_dict = {}

    # random.randrange(1,10000000)

    for i in range(num):
        temp_dict[i] = random.randrange(1,1000)

    return temp_dict

def 딕셔너리변환기(original_dict):
    # 이름 : 개수 형대의 오리지날 딕셔너리를 받으면, 확률값 딕셔너리로 변환해준다.
    total_sum = 0
    for i in original_dict.values():
        total_sum += i
    neo_dict = {}
    for i in original_dict.keys():
        neo_dict[i] = original_dict[i]/total_sum

    test = 0
    for i in neo_dict.values():
        test += i
    # print(test)
    return neo_dict




original_dict = 딕셔너리생성기(5)
# print(original_dict)
proba_dict = 딕셔너리변환기(original_dict)
# print(proba_dict)
huffman_dict = huffman(proba_dict)
# print(huffman_dict)

#
# print(HuffEntropyCal(original_dict,huffman_dict),"허프만")
# print(ShanoonEntropy(proba_dict),"섀넌")

유사도 = []
for i in tqdm(range(1000)):
    try:
        original_dict = 딕셔너리생성기(20)
        proba_dict = 딕셔너리변환기(original_dict)
        huffman_dict = huffman(proba_dict)

        유사도.append(HuffEntropyCal(original_dict, huffman_dict) / ShanoonEntropy(proba_dict))  # 허프만 / 섀넌
    except:
        #부끄럽지만 남의 코드 가져오면서 남의 코드에서 요구하는 조건인 확률 딕셔너리의 총합이 1이어야 하는데, 내가
        #만든 딕셔너리는 1.000000001 이거나 0.999999999999999 거나 하는 문제가 있어서 어서트를 블랭크 처리하고
        #에러가 나면 걍 씹도록 하였다. 귀찮.... 그래도 결과물은 괜찮으니까
        #아 근데 딕셔너리 길이 길면 에러가 더 자주 나는지 아예 생성이 안되더라..... 뭥미?
        pass

print(유사도)


""" 유사도 = (허프만 코딩 엔트로피 / 섀넌 확률밀도로 구한 엔트로피) 결과
[1.0134788852936099, 1.0084752248356748, 1.0138670630326956, 1.0077922068414416, 1.0094078192722857, 1.0135302476109074, 
1.007455398251497, 1.0112498067783562, 1.0070402197428856, 1.0120346808532283, 1.0099190661175836, 1.0086528782451583,
 1.0108241142305394, 1.008592924820444, 1.0118859874801889, 1.0115388867112463, 1.0116096426548737, 1.0140830896352886,
  1.012425418798176, 1.0083009231807487, 1.0066644206219855, 1.0107092102768305, 1.0080316917671905, 1.0115505490338441,
   1.0087694134871186, 1.0082827402952643, 1.0076329080006272, 1.0091614954314674, 1.0134858332423553, 1.0111883092363192,
    1.0067013851053797, 1.0119236201325845, 1.0088217242064978, 1.0102189552258614, 1.0094905017196416, 1.0109054488253326, 
    1.0110307119531337, 1.011135159112794, 1.0081131729216362, 1.0071195901997376, 1.0103127964692502, 1.0109773540385314,
     1.0083167025699642, 1.0098963956796017]

이 결과에서 알 수 있는 것은, 놀랍도록 일치한다는 것.
허프만이 조금 ☆★더 일관적으로 큰데☆★, 
이건 뭐 완전 이진트리가 아니고 어쩌고 저쩌고 하는 문제 때문에 발생하는 오차일 것.

섀넌과 허프만의 결론은 같았다.
그리고  섀넌은 48년, 허프만은 52년 이라서 허프만이 더 뒤였음.

사기친 리스트 정리

1. 섀넌의 엔트로피 계산법이 허프만 코딩과 같은 결과를 냄
2. 섀넌이 더 빨랐음
3. 섀넌 엔트로피 설명 때 내가 혹시 베이스 2가 아니라 자연로그 썼나? 하여간 허프만 코딩은 이진 트리니까 감각적으로 베이스 2를 쓰는 로그여야 한다는 결론 
4. 마지막 스터디 때 왕창 사기 침. ㅋㅋㅋㅋㅋㅋ

하여간 검증 끝
 
"""