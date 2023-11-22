package com.ilegra.labs.author.contract.v1;

public class Author {
    private String id;
    private String name;
    private String birthDate;


    public Author()  {     }
    public Author(String id, String name, String birthDate) {
        this.birthDate = birthDate;
        this.id = id;
        this.name =  name;
    }

    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getName() {
        return name;
    }
    public void setBirthDate(String birthDate) {
        this.birthDate = birthDate;
    }

    public String getBirthDate() {
        return birthDate;
    }
}
