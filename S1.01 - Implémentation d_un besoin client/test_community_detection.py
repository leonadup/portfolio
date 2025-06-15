def test_create_network():
    assert create_network(liste_amis) == {"Dominique": ["Alice"] , "Alice" : ["Dominique"] }
    assert create_network(encoreee) =={"Alice":["Bob","Charlie"],"Bob":["Alice"],"Charlie":["Alice"]    }
    print("Test OK")
    
test_create_network()

def test_get_people():
    assert get_people(dico) == ["Dominique","Charlie","Bob"]
    assert get_people(dico2) == ["Alice", "Bob", "Charlie", "Dominique"]
    print("Test OK")
    
test_create_network()

def test_are_friends() : 
    assert are_friends(dico3,"Alice","Dominique") == True
    assert are_friends(dico3,"Dominique","Charlie") == False
    print("Test OK")
    
test_are_friends()

def test_all_his_friends():
    assert all_his_friends(dico,"Charlie",tab) == False
    assert all_his_friends(dico,"Alice",tab) == True
    print("Test OK")
    
test_all_his_friends()

def test_is_a_community():
    assert is_a_community(dico,tab) == False
    assert is_a_community(dico,tab2) == True
    print("Test OK")
    
test_is_a_community()

def test_find_community():
    assert find_community(dico,groupeUno) == ["Alice", "Bob", "Dominique"]
    assert find_community(dico,groupeDeux) == ["Charlie", "Bob"]
    print("Test OK")
    
test_find_community()

def test_order_by_decreasing_popularity():
    assert order_by_decreasing_popularity(dico,Graoupe) == ["Bob", "Alice", "Charlie"]
    assert order_by_decreasing_popularity(dico,Graoupe2) == ["Dominque","Charlie"]
    print("Test OK")

test_order_by_decreasing_popularity