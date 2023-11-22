package com.ilegra.labs.book.contract.v1;

public class Book {
    private String id;
    private String authorId;
    private String title;
    private String year;

    private String isbn;

    public Book()  {     }

    public Book(String id, String authorId, String title, String year, String isbn) {
        this.id = id;
        this.authorId = authorId;
        this.title = title;
        this.year = year;
        this.isbn = isbn;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getAuthorId() {
        return authorId;
    }

    public void setAuthorId(String authorId) {
        this.authorId = authorId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getYear() {
        return year;
    }

    public void setYear(String year) {
        this.year = year;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }
}
