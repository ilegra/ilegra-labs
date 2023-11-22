package com.ilegra.labs.author.repository;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.Date;

@Table( name =  "author")
@Entity
public class AuthorEntity {
    @Id
    private String id;
    @Column(name  = "name")
    private String name;
    @Column(name  = "birth_date")
    private Date birthDate;

    public AuthorEntity() {}

    public AuthorEntity(String id, String name, Date birthDate) {
        this.id = id;
        this.name = name;
        this.birthDate = birthDate;
    }

    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public void setBirthDate(Date birthDate) {
        this.birthDate = birthDate;
    }
    public Date getBirthDate() {
        return birthDate;
    }
}
