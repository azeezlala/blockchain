// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 public favoriteNumber = 5;
    //bool favoriteBool = false;
    //string favoriteString = "String";
    //int256 favoriteInt = -5;
    //address favoriteAddress = 0xc8C582e24e4b9d729889067457cC342fEbb58c55;
    //bytes32 favoriteBytes = "cat";
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People public person = People({favoriteNumber: 2, name: "Lala"});

    //People[1] public listOfPeople;
    People[] public listOfPeople;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns(uint256){
        return favoriteNumber;
    }

    function getFavNumber(uint256 favoriteNumber) public pure {
        favoriteNumber + favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        listOfPeople.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}