import sys, os
from pathlib import Path

CODE = Path("C:/Users/made1/alive-engineering-standard/templates/code")

TEMPLATES = {
    "spring": {
        "mapper.java.j2": """package com.alive.{{ entity_lower }}.mapper;

import com.alive.{{ entity_lower }}.{{ entity }};
import com.alive.{{ entity_lower }}.dto.{{ entity }}DTO;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface {{ entity }}Mapper {
    {{ entity }} toEntity({{ entity }}DTO dto);
    {{ entity }}DTO toDTO({{ entity }} entity);
}""",
        "config.java.j2": """package com.alive.{{ entity_lower }}.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@Configuration
@EnableConfigurationProperties
public class {{ entity }}Config {
}""",
        "exception.java.j2": """package com.alive.{{ entity_lower }}.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class {{ entity }}NotFoundException extends RuntimeException {
    public {{ entity }}NotFoundException(Long id) {
        super("{{ entity }} not found: " + id);
    }
}""",
        "validation.java.j2": """package com.alive.{{ entity_lower }}.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.*;

@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = {{ entity }}Validator.class)
public @interface Valid{{ entity }} {
    String message() default "Invalid {{ entity_lower }}";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}""",
        "scheduler.java.j2": """package com.alive.{{ entity_lower }}.scheduler;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class {{ entity }}Scheduler {
    private final {{ entity }}Service {{ entity_lower }}Service;

    @Scheduled(cron = "0 0 * * * *")
    public void process{{ entity }}() {
        log.info("Scheduled task started: {{ entity_lower }} processing");
        {{ entity_lower }}Service.process();
    }
}""",
        "event.java.j2": """package com.alive.{{ entity_lower }}.event;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class {{ entity }}CreatedEvent extends ApplicationEvent {
    private final Long {{ entity_lower }}Id;

    public {{ entity }}CreatedEvent(Object source, Long {{ entity_lower }}Id) {
        super(source);
        this.{{ entity_lower }}Id = {{ entity_lower }}Id;
    }
}""",
        "filter.java.j2": """package com.alive.{{ entity_lower }}.filter;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import java.io.IOException;

@Slf4j
@Component
public class {{ entity }}Filter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        log.debug("{{ entity }} filter: {}", req.getRequestURI());
        chain.doFilter(request, response);
    }
}""",
        "util.java.j2": """package com.alive.{{ entity_lower }}.util;

import lombok.experimental.UtilityClass;
import java.util.UUID;

@UtilityClass
public class {{ entity }}Utils {
    public String generate{{ entity }}Id() {
        return "{{ entity_lower }}-" + UUID.randomUUID().toString().substring(0, 8);
    }
}""",
        "test.java.j2": """package com.alive.{{ entity_lower }};

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class {{ entity }}ServiceTest {
    @Autowired
    private {{ entity }}Service {{ entity_lower }}Service;

    @Test
    void shouldCreate{{ entity }}() {
        var result = {{ entity_lower }}Service.create(new {{ entity }}());
        assertThat(result).isNotNull();
    }
}""",
        "application.yml.j2": """spring:
  application:
    name: {{ entity_lower }}-service
  datasource:
    url: jdbc:postgresql://localhost:5432/{{ entity_lower }}
    username: ${DB_USERNAME:app}
    password: ${DB_PASSWORD:secret}
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false""",
    },
    "flutter": {
        "screen.dart.j2": """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/{{ entity_lower }}_provider.dart';

class {{ entity }}Screen extends ConsumerWidget {
  const {{ entity }}Screen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch({{ entity_lower }}Provider);
    return Scaffold(
      appBar: AppBar(title: const Text('{{ entity }}')),
      body: Center(child: Text('{{ entity }} Content')),
    );
  }
}""",
        "widget.dart.j2": """import 'package:flutter/material.dart';

class {{ entity }}Widget extends StatelessWidget {
  final String title;
  final VoidCallback? onTap;

  const {{ entity }}Widget({super.key, required this.title, this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(title),
        onTap: onTap,
      ),
    );
  }
}""",
        "repository.dart.j2": """import 'package:dio/dio.dart';
import '../models/{{ entity_lower }}.dart';

class {{ entity }}Repository {
  final Dio _dio;

  {{ entity }}Repository(this._dio);

  Future<List<{{ entity }}>> fetchAll() async {
    final response = await _dio.get('/{{ entity_lower }}s');
    return (response.data as List).map((e) => {{ entity }}.fromJson(e)).toList();
  }

  Future<{{ entity }}> fetchById(int id) async {
    final response = await _dio.get('/{{ entity_lower }}s/\$id');
    return {{ entity }}.fromJson(response.data);
  }
}""",
        "bloc.dart.j2": """import 'package:flutter_bloc/flutter_bloc.dart';
import '../../repositories/{{ entity_lower }}_repository.dart';
import '../../models/{{ entity_lower }}.dart';

sealed class {{ entity }}State {}
final class {{ entity }}Initial extends {{ entity }}State {}
final class {{ entity }}Loaded extends {{ entity }}State {
  final List<{{ entity }}> items;
  {{ entity }}Loaded(this.items);
}
final class {{ entity }}Error extends {{ entity }}State {
  final String message;
  {{ entity }}Error(this.message);
}

class {{ entity }}Cubit extends Cubit<{{ entity }}State> {
  final {{ entity }}Repository _repository;
  {{ entity }}Cubit(this._repository) : super({{ entity }}Initial());

  void load() async {
    emit({{ entity }}Initial());
    try {
      final items = await _repository.fetchAll();
      emit({{ entity }}Loaded(items));
    } catch (e) {
      emit({{ entity }}Error(e.toString()));
    }
  }
}""",
        "route.dart.j2": """import 'package:flutter/material.dart';
import '../screens/{{ entity_lower }}_screen.dart';

class {{ entity }}Router {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/{{ entity_lower }}s':
        return MaterialPageRoute(builder: (_) => const {{ entity }}Screen());
      default:
        return MaterialPageRoute(
          builder: (_) => const Scaffold(body: Text('Route not found')),
        );
    }
  }
}""",
        "theme.dart.j2": """import 'package:flutter/material.dart';

class {{ entity }}Theme {
  static ThemeData get light => ThemeData(
    colorSchemeSeed: Colors.blue,
    useMaterial3: true,
    brightness: Brightness.light,
  );

  static ThemeData get dark => ThemeData(
    colorSchemeSeed: Colors.blue,
    useMaterial3: true,
    brightness: Brightness.dark,
  );
}""",
        "util.dart.j2": """class {{ entity }}Validator {
  static String? validateName(String? value) {
    if (value == null || value.isEmpty) return 'Name required';
    if (value.length < 2) return 'Name too short';
    return null;
  }

  static String? validateEmail(String? value) {
    if (value == null || value.isEmpty) return 'Email required';
    if (!value.contains('@')) return 'Invalid email';
    return null;
  }
}""",
        "api_client.dart.j2": """import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

class {{ entity }}ApiClient {
  late final Dio _dio;

  {{ entity }}ApiClient({required String baseUrl}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ));
    _dio.interceptors.add(LogInterceptor(
      requestBody: kDebugMode,
      responseBody: kDebugMode,
    ));
  }

  Dio get dio => _dio;
}""",
        "model_freezed.dart.j2": """import 'package:freezed_annotation/freezed_annotation.dart';
part '{{ entity_lower }}.freezed.dart';
part '{{ entity_lower }}.g.dart';

@freezed
class {{ entity }} with _\${{ entity }} {
  const factory {{ entity }}(
    int id,
    String name,
    String? description,
  ) = _{{ entity }};

  factory {{ entity }}.fromJson(Map<String, dynamic> json) =>
      _\${{ entity }}FromJson(json);
}""",
        "l10n.dart.j2": """import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

extension {{ entity }}L10n on BuildContext {
  AppLocalizations get l10n => AppLocalizations.of(this)!;
}""",
    },
    "go": {
        "service.go.j2": """package {{ entity_lower }}

import "context"

type Service struct {
    repo *Repository
}

func NewService(repo *Repository) *Service {
    return &Service{repo: repo}
}

func (s *Service) Create(ctx context.Context, entity *{{ entity }}) (*{{ entity }}, error) {
    return s.repo.Create(ctx, entity)
}

func (s *Service) Get(ctx context.Context, id int64) (*{{ entity }}, error) {
    return s.repo.FindByID(ctx, id)
}""",
        "middleware.go.j2": """package {{ entity_lower }}

import (
    "net/http"
    "strings"
    "github.com/gin-gonic/gin"
)

func {{ entity }}Middleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if !strings.HasPrefix(token, "Bearer ") {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
            return
        }
        c.Next()
    }
}""",
        "router.go.j2": """package {{ entity_lower }}

import "github.com/gin-gonic/gin"

func Register{{ entity }}Routes(r *gin.RouterGroup, h *Handler) {
    r.GET("/{{ entity_lower }}s", h.List)
    r.GET("/{{ entity_lower }}s/:id", h.Get)
    r.POST("/{{ entity_lower }}s", h.Create)
    r.PUT("/{{ entity_lower }}s/:id", h.Update)
    r.DELETE("/{{ entity_lower }}s/:id", h.Delete)
}""",
        "config.go.j2": """package config

import (
    "os"
    "strconv"
)

type {{ entity }}Config struct {
    Port    int
    DBHost  string
    DBPort  int
    DBUser  string
    DBPass  string
    DBName  string
}

func Load{{ entity }}Config() *{{ entity }}Config {
    port, _ := strconv.Atoi(getEnv("PORT", "8080"))
    dbPort, _ := strconv.Atoi(getEnv("DB_PORT", "5432"))
    return &{{ entity }}Config{
        Port:   port,
        DBHost: getEnv("DB_HOST", "localhost"),
        DBPort: dbPort,
        DBUser: getEnv("DB_USER", "postgres"),
        DBName: getEnv("DB_NAME", "{{ entity_lower }}"),
    }
}

func getEnv(key, fallback string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return fallback
}""",
        "migration.go.j2": """package migration

import (
    "database/sql"
    "fmt"
    _ "github.com/lib/pq"
)

func Run{{ entity }}Migration(db *sql.DB) error {
    query := fmt.Sprintf(`
        CREATE TABLE IF NOT EXISTS {{ entity_lower }}s (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )`)
    _, err := db.Exec(query)
    return err
}""",
        "test.go.j2": """package {{ entity_lower }}

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestCreate{{ entity }}(t *testing.T) {
    mockRepo := new(MockRepository)
    svc := NewService(mockRepo)
    entity := &{{ entity }}{Name: "test"}
    mockRepo.On("Create", entity).Return(entity, nil)
    result, err := svc.Create(nil, entity)
    assert.NoError(t, err)
    assert.Equal(t, "test", result.Name)
}""",
        "dto.go.j2": """package {{ entity_lower }}

type Create{{ entity }}Request struct {
    Name        string `+"`"+`json:"name" binding:"required"`+"`"+`
    Description string `+"`"+`json:"description"`+"`"+`
}

type {{ entity }}Response struct {
    ID          int64  `+"`"+`json:"id"`+"`"+`
    Name        string `+"`"+`json:"name"`+"`"+`
    Description string `+"`"+`json:"description"`+"`"+`
    CreatedAt   string `+"`"+`json:"created_at"`+"`"+`
}

func To{{ entity }}Response(entity *{{ entity }}) *{{ entity }}Response {
    return &{{ entity }}Response{
        ID:          entity.ID,
        Name:        entity.Name,
        Description: entity.Description,
    }
}""",
        "error.go.j2": """package {{ entity_lower }}

import "errors"

var (
    ErrNotFound         = errors.New("{{ entity_lower }} not found")
    ErrInvalidInput     = errors.New("invalid input")
    ErrDuplicateEntry   = errors.New("duplicate entry")
)

type {{ entity }}Error struct {
    Code    string `+"`"+`json:"code"`+"`"+`
    Message string `+"`"+`json:"message"`+"`"+`
}

func (e *{{ entity }}Error) Error() string {
    return e.Message
}""",
        "logger.go.j2": """package logger

import (
    "log/slog"
    "os"
)

var Log *slog.Logger

func Init() {
    handler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    })
    Log = slog.New(handler)
}""",
    },
    "kotlin": {
        "controller.kt.j2": """package com.alive.{{ entity_lower }}.controller

import com.alive.{{ entity_lower }}.{{ entity }}
import com.alive.{{ entity_lower }}.service.{{ entity }}Service
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/v1/{{ entity_lower }}s")
class {{ entity }}Controller(private val service: {{ entity }}Service) {

    @GetMapping
    fun findAll(): List<{{ entity }}> = service.findAll()

    @GetMapping("/{id}")
    fun findById(@PathVariable id: Long): {{ entity }} = service.findById(id)

    @PostMapping
    fun create(@RequestBody entity: {{ entity }}): {{ entity }} = service.save(entity)
}""",
        "service.kt.j2": """package com.alive.{{ entity_lower }}.service

import com.alive.{{ entity_lower }}.{{ entity }}
import com.alive.{{ entity_lower }}.repository.{{ entity }}Repository
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
@Transactional
class {{ entity }}Service(private val repository: {{ entity }}Repository) {

    fun findAll(): List<{{ entity }}> = repository.findAll()

    fun findById(id: Long): {{ entity }} = repository.findById(id)
        .orElseThrow { RuntimeException("{{ entity }} not found") }

    fun save(entity: {{ entity }}): {{ entity }} = repository.save(entity)
}""",
        "repository.kt.j2": """package com.alive.{{ entity_lower }}.repository

import com.alive.{{ entity_lower }}.{{ entity }}
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface {{ entity }}Repository : JpaRepository<{{ entity }}, Long> {
    fun findByNameContaining(name: String): List<{{ entity }}>
}""",
        "dto.kt.j2": """package com.alive.{{ entity_lower }}.dto

data class {{ entity }}Request(
    val name: String,
    val description: String? = null
)

data class {{ entity }}Response(
    val id: Long,
    val name: String,
    val description: String?,
    val createdAt: String
)""",
        "config.kt.j2": """package com.alive.{{ entity_lower }}.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class {{ entity }}Config {
    @Bean
    fun {{ entity_lower }}CacheProvider(): CacheProvider = InMemoryCacheProvider()
}

interface CacheProvider
class InMemoryCacheProvider : CacheProvider""",
        "extension.kt.j2": """package com.alive.{{ entity_lower }}.extension

fun String.to{{ entity }}Slug(): String =
    this.lowercase().replace(Regex("[^a-z0-9]+"), "-").trim('-')

fun Long.to{{ entity }}IdString(): String =
    "{{ entity_lower }}-$this"
""",
        "exception.kt.j2": """package com.alive.{{ entity_lower }}.exception

class {{ entity }}NotFoundException(id: Long) : RuntimeException("{{ entity }} not found: $id")
class {{ entity }}ValidationException(message: String) : RuntimeException(message)

data class ErrorResponse(
    val code: String,
    val message: String,
    val timestamp: Long = System.currentTimeMillis()
)""",
        "mapper.kt.j2": """package com.alive.{{ entity_lower }}.mapper

import com.alive.{{ entity_lower }}.{{ entity }}
import com.alive.{{ entity_lower }}.dto.{{ entity }}Request
import com.alive.{{ entity_lower }}.dto.{{ entity }}Response
import org.mapstruct.Mapper

@Mapper(componentModel = "spring")
interface {{ entity }}Mapper {
    fun toEntity(request: {{ entity }}Request): {{ entity }}
    fun toResponse(entity: {{ entity }}): {{ entity }}Response
}""",
        "test.kt.j2": """package com.alive.{{ entity_lower }}

import com.alive.{{ entity_lower }}.service.{{ entity }}Service
import io.kotest.core.spec.style.BehaviorSpec
import io.kotest.matchers.shouldNotBe
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest
class {{ entity }}ServiceTest(private val service: {{ entity }}Service) : BehaviorSpec({
    Given("a valid {{ entity_lower }}") {
        When("creating") {
            val result = service.save({{ entity }}())
            Then("should succeed") {
                result shouldNotBe null
            }
        }
    }
})""",
        "security.kt.j2": """package com.alive.{{ entity_lower }}.security

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.web.SecurityFilterChain

@Configuration
class {{ entity }}SecurityConfig {
    @Bean
    fun filterChain(http: HttpSecurity): SecurityFilterChain = http
        .authorizeHttpRequests { auth ->
            auth.requestMatchers("/api/v1/{{ entity_lower }}s/**").authenticated()
        }
        .oauth2ResourceServer { it.jwt {} }
        .build()
}""",
    },
    "react": {
        "context.tsx.j2": """import React, { createContext, useContext, useState, ReactNode } from 'react';
import type { {{ entity }} } from './types';

interface {{ entity }}ContextValue {
  items: {{ entity }}[];
  addItem: (item: {{ entity }}) => void;
  removeItem: (id: number) => void;
}

const {{ entity }}Context = createContext<{{ entity }}ContextValue | undefined>(undefined);

export function {{ entity }}Provider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<{{ entity }}[]>([]);

  const addItem = (item: {{ entity }}) => setItems(prev => [...prev, item]);
  const removeItem = (id: number) => setItems(prev => prev.filter(i => i.id !== id));

  return (
    <{{ entity }}Context.Provider value={{ items, addItem, removeItem }}>
      {children}
    </{{ entity }}Context.Provider>
  );
}

export function use{{ entity }}Context() {
  const ctx = useContext({{ entity }}Context);
  if (!ctx) throw new Error('{{ entity }}Context not found');
  return ctx;
}""",
        "reducer.ts.j2": """import type { {{ entity }} } from './types';

type Action =
  | { type: 'SET_ITEMS'; payload: {{ entity }}[] }
  | { type: 'ADD_ITEM'; payload: {{ entity }} }
  | { type: 'REMOVE_ITEM'; payload: number }
  | { type: 'SET_LOADING'; payload: boolean };

export interface {{ entity }}State {
  items: {{ entity }}[];
  loading: boolean;
  error: string | null;
}

export const initial{{ entity }}State: {{ entity }}State = {
  items: [],
  loading: false,
  error: null,
};

export function {{ entity_lower }}Reducer(state: {{ entity }}State, action: Action): {{ entity }}State {
  switch (action.type) {
    case 'SET_ITEMS': return { ...state, items: action.payload, loading: false };
    case 'ADD_ITEM': return { ...state, items: [...state.items, action.payload] };
    case 'REMOVE_ITEM': return { ...state, items: state.items.filter(i => i.id !== action.payload) };
    case 'SET_LOADING': return { ...state, loading: action.payload };
    default: return state;
  }
}""",
        "util.ts.j2": """import type { {{ entity }} } from './types';

export function format{{ entity }}Name(item: {{ entity }}): string {
  return item.name.charAt(0).toUpperCase() + item.name.slice(1);
}

export function filter{{ entity }}s(items: {{ entity }}[], query: string): {{ entity }}[] {
  return items.filter(i =>
    i.name.toLowerCase().includes(query.toLowerCase())
  );
}

export function sort{{ entity }}s(items: {{ entity }}[], key: keyof {{ entity }}): {{ entity }}[] {
  return [...items].sort((a, b) => String(a[key]).localeCompare(String(b[key])));
}""",
        "layout.tsx.j2": """import React from 'react';
import { Outlet } from 'react-router-dom';
import { {{ entity }}Provider } from './context';
import { {{ entity }}Header } from './header';
import { {{ entity }}Sidebar } from './sidebar';

export function {{ entity }}Layout() {
  return (
    <{{ entity }}Provider>
      <div className="{{ entity_lower }}-layout">
        <{{ entity }}Header />
        <div className="{{ entity_lower }}-body">
          <{{ entity }}Sidebar />
          <main className="{{ entity_lower }}-content">
            <Outlet />
          </main>
        </div>
      </div>
    </{{ entity }}Provider>
  );
}""",
        "page.tsx.j2": """import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import type { {{ entity }} } from './types';
import { {{ entity_lower }}Api } from './api';
import { {{ entity }}List } from './components/{{ entity_lower }}-list';

export function {{ entity }}Page() {
  const [items, setItems] = useState<{{ entity }}[]>([]);
  const { id } = useParams();

  useEffect(() => {
    {{ entity_lower }}Api.list().then(setItems);
  }, [id]);

  return (
    <div className="{{ entity_lower }}-page">
      <h1>{{ entity }} Management</h1>
      <{{ entity }}List items={items} />
    </div>
  );
}""",
        "service.ts.j2": """import type { {{ entity }} } from './types';

const API_BASE = '/api/v1/{{ entity_lower }}s';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export const {{ entity_lower }}Api = {
  list: (): Promise<{{ entity }}[]> => request(API_BASE),
  get: (id: number): Promise<{{ entity }}> => request(`${API_BASE}/${id}`),
  create: (data: Partial<{{ entity }}>): Promise<{{ entity }}> =>
    request(API_BASE, { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<{{ entity }}>): Promise<{{ entity }}> =>
    request(`${API_BASE}/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number): Promise<void> =>
    request(`${API_BASE}/${id}`, { method: 'DELETE' }),
};""",
        "store.ts.j2": """import { create } from 'zustand';
import type { {{ entity }} } from './types';
import { {{ entity_lower }}Api } from './api';

interface {{ entity }}Store {
  items: {{ entity }}[];
  loading: boolean;
  error: string | null;
  fetch: () => Promise<void>;
  add: (data: Partial<{{ entity }}>) => Promise<void>;
  remove: (id: number) => Promise<void>;
}

export const use{{ entity }}Store = create<{{ entity }}Store>((set) => ({
  items: [],
  loading: false,
  error: null,

  fetch: async () => {
    set({ loading: true });
    try {
      const items = await {{ entity_lower }}Api.list();
      set({ items, loading: false });
    } catch (e) {
      set({ error: String(e), loading: false });
    }
  },

  add: async (data) => {
    const item = await {{ entity_lower }}Api.create(data);
    set((s) => ({ items: [...s.items, item] }));
  },

  remove: async (id) => {
    await {{ entity_lower }}Api.delete(id);
    set((s) => ({ items: s.items.filter((i) => i.id !== id) }));
  },
}));""",
        "test.tsx.j2": """import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { {{ entity }}List } from './components/{{ entity_lower }}-list';

const mockItems = [
  { id: 1, name: 'Item 1' },
  { id: 2, name: 'Item 2' },
];

describe('{{ entity }}List', () => {
  it('renders items', () => {
    render(<{{ entity }}List items={mockItems} />);
    expect(screen.getByText('Item 1')).toBeDefined();
    expect(screen.getByText('Item 2')).toBeDefined();
  });

  it('handles empty state', () => {
    render(<{{ entity }}List items={[]} />);
    expect(screen.getByText(/no {{ entity_lower }}s/i)).toBeDefined();
  });
});""",
        "types.ts.j2": """export interface {{ entity }} {
  id: number;
  name: string;
  description?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface {{ entity }}CreateInput {
  name: string;
  description?: string;
}

export interface {{ entity }}UpdateInput extends Partial<{{ entity }}CreateInput> {
  id: number;
}

export interface {{ entity }}Filter {
  search?: string;
  page?: number;
  limit?: number;
}""",
        "index.ts.j2": """export { {{ entity }}List } from './components/{{ entity_lower }}-list';
export { {{ entity }}Form } from './components/{{ entity_lower }}-form';
export { {{ entity }}Page } from './{{ entity_lower }}-page';
export { {{ entity }}Layout } from './{{ entity_lower }}-layout';
export { {{ entity }}Provider, use{{ entity }}Context } from './context';
export { {{ entity_lower }}Reducer, initial{{ entity }}State } from './reducer';
export { {{ entity_lower }}Api } from './api';
export type { {{ entity }}, {{ entity }}CreateInput, {{ entity }}Filter } from './types';""",
    },
    "rust": {
        "repository.rs.j2": """use sqlx::PgPool;
use crate::models::{{ entity }};

pub struct {{ entity }}Repository {
    pool: PgPool,
}

impl {{ entity }}Repository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    pub async fn find_all(&self) -> Result<Vec<{{ entity }}>, sqlx::Error> {
        sqlx::query_as::<_, {{ entity }}>("SELECT * FROM {{ entity_lower }}s")
            .fetch_all(&self.pool)
            .await
    }

    pub async fn find_by_id(&self, id: i64) -> Result<Option<{{ entity }}>, sqlx::Error> {
        sqlx::query_as("SELECT * FROM {{ entity_lower }}s WHERE id = $1")
            .bind(id)
            .fetch_optional(&self.pool)
            .await
    }
}""",
        "service.rs.j2": """use crate::models::{{ entity }};
use crate::repositories::{{ entity }}Repository;

pub struct {{ entity }}Service {
    repo: {{ entity }}Repository,
}

impl {{ entity }}Service {
    pub fn new(repo: {{ entity }}Repository) -> Self {
        Self { repo }
    }

    pub async fn list(&self) -> Result<Vec<{{ entity }}>, String> {
        self.repo.find_all().await.map_err(|e| e.to_string())
    }

    pub async fn get(&self, id: i64) -> Result<{{ entity }}, String> {
        self.repo
            .find_by_id(id)
            .await
            .map_err(|e| e.to_string())?
            .ok_or_else(|| "Not found".to_string())
    }
}""",
        "config.rs.j2": """use std::env;

#[derive(Clone)]
pub struct {{ entity }}Config {
    pub database_url: String,
    pub host: String,
    pub port: u16,
    pub log_level: String,
}

impl {{ entity }}Config {
    pub fn from_env() -> Result<Self, env::VarError> {
        Ok(Self {
            database_url: env::var("DATABASE_URL")?,
            host: env::var("HOST").unwrap_or_else(|_| "0.0.0.0".into()),
            port: env::var("PORT")
                .unwrap_or_else(|_| "8080".into())
                .parse()
                .unwrap_or(8080),
            log_level: env::var("LOG_LEVEL").unwrap_or_else(|_| "info".into()),
        })
    }
}""",
        "middleware.rs.j2": """use axum::{
    http::Request,
    middleware::Next,
    response::Response,
};

pub async fn {{ entity_lower }}_middleware<B>(req: Request<B>, next: Next<B>) -> Response {
    tracing::info!("{{ entity }} middleware: {} {}", req.method(), req.uri());
    next.run(req).await
}""",
        "error.rs.j2": """use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;

#[derive(Debug)]
pub enum {{ entity }}Error {
    NotFound,
    BadRequest(String),
    Internal(String),
}

impl IntoResponse for {{ entity }}Error {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            Self::NotFound => (StatusCode::NOT_FOUND, "Not found".into()),
            Self::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg),
            Self::Internal(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg),
        };
        (status, Json(json!({ "error": message }))).into_response()
    }
}""",
        "test.rs.j2": """use axum_test::TestServer;
use crate::routes::app;

#[tokio::test]
async fn test_list_{{ entity_lower }}s() {
    let app = app().await;
    let server = TestServer::new(app).unwrap();
    let res = server.get("/api/{{ entity_lower }}s").await;
    assert_eq!(res.status_code(), 200);
}

#[tokio::test]
async fn test_create_{{ entity_lower }}() {
    let app = app().await;
    let server = TestServer::new(app).unwrap();
    let res = server
        .post("/api/{{ entity_lower }}s")
        .json(&serde_json::json!({"name": "test"}))
        .await;
    assert_eq!(res.status_code(), 201);
}""",
        "schema.rs.j2": """use serde::{Deserialize, Serialize};
use sqlx::FromRow;

#[derive(Debug, Serialize, Deserialize, FromRow)]
pub struct {{ entity }} {
    pub id: i64,
    pub name: String,
    pub description: Option<String>,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub updated_at: Option<chrono::DateTime<chrono::Utc>>,
}""",
        "main.rs.j2": """mod config;
mod errors;
mod handlers;
mod models;
mod repositories;
mod routes;
mod services;

use std::net::SocketAddr;
use config::{{ entity }}Config;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();
    let cfg = {{ entity }}Config::from_env().expect("config");
    let addr = SocketAddr::new(cfg.host.parse().unwrap(), cfg.port);
    tracing::info!("starting on {}", addr);
    let app = routes::app().await;
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}""",
        "migration.rs.j2": """use sqlx::migrate::Migrator;
use std::path::Path;

pub async fn run_migrations(pool: &sqlx::PgPool) {
    let migrator = Migrator::new(Path::new("./migrations")).await.unwrap();
    migrator.run(pool).await.unwrap();
    tracing::info!("migrations complete");
}""",
        "dto.rs.j2": """use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct Create{{ entity }}Request {
    pub name: String,
    pub description: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct {{ entity }}Response {
    pub id: i64,
    pub name: String,
    pub description: Option<String>,
}

impl From<crate::models::{{ entity }}> for {{ entity }}Response {
    fn from(e: crate::models::{{ entity }}) -> Self {
        Self {
            id: e.id,
            name: e.name,
            description: e.description,
        }
    }
}""",
    },
    "vue3": {
        "component.vue.j2": """<template>
  <div class="{{ entity_lower }}-card">
    <h3>{{ item.name }}</h3>
    <p v-if="item.description">{{ item.description }}</p>
    <slot name="actions" :item="item" />
  </div>
</template>

<script setup lang="ts">
import type { {{ entity }} } from './types';

interface Props {
  item: {{ entity }};
}

defineProps<Props>();
</script>

<style scoped>
.{{ entity_lower }}-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
}
</style>""",
        "store.ts.j2": """import { defineStore } from 'pinia';
import { ref } from 'vue';
import { {{ entity_lower }}Api } from './api';
import type { {{ entity }} } from './types';

export const use{{ entity }}Store = defineStore('{{ entity_lower }}', () => {
  const items = ref<{{ entity }}[]>([]);
  const loading = ref(false);

  async function fetchAll() {
    loading.value = true;
    try {
      items.value = await {{ entity_lower }}Api.list();
    } finally {
      loading.value = false;
    }
  }

  async function create(data: Partial<{{ entity }}>) {
    const item = await {{ entity_lower }}Api.create(data);
    items.value.push(item);
  }

  return { items, loading, fetchAll, create };
});""",
        "router.ts.j2": """import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/{{ entity_lower }}s',
    name: '{{ entity }}List',
    component: () => import('./pages/{{ entity_lower }}-list.vue'),
  },
  {
    path: '/{{ entity_lower }}s/:id',
    name: '{{ entity }}Detail',
    component: () => import('./pages/{{ entity_lower }}-detail.vue'),
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});""",
        "util.ts.j2": """import type { {{ entity }} } from './types';

export function format{{ entity }}Date(date: string): string {
  return new Date(date).toLocaleDateString('zh-CN');
}

export function validate{{ entity }}(data: Partial<{{ entity }}>): Record<string, string> {
  const errors: Record<string, string> = {};
  if (!data.name?.trim()) errors.name = '名称必填';
  return errors;
}""",
        "directive.ts.j2": """import type { Directive } from 'vue';

export const v{{ entity }}Highlight: Directive = {
  mounted(el: HTMLElement) {
    el.style.transition = 'background-color 0.3s';
  },
};

export const v{{ entity }}Permission: Directive<HTMLElement, string[]> = {
  mounted(el, binding) {
    const userPermissions = JSON.parse(localStorage.getItem('permissions') || '[]');
    if (!binding.value.some((p: string) => userPermissions.includes(p))) {
      el.remove();
    }
  },
};""",
        "plugin.ts.j2": """import type { App } from 'vue';

export default {
  install(app: App) {
    app.config.globalProperties.${{ entity_lower }} = {
      version: '1.0.0',
      config: {
        baseUrl: import.meta.env.VITE_API_BASE || '/api',
      },
    };
  },
};""",
        "layout.vue.j2": """<template>
  <div class="{{ entity_lower }}-layout">
    <header class="layout-header">
      <h1>{{ entity }} Manager</h1>
      <nav>
        <router-link to="/{{ entity_lower }}s">列表</router-link>
        <router-link to="/{{ entity_lower }}s/create">新建</router-link>
      </nav>
    </header>
    <main class="layout-main">
      <router-view />
    </main>
  </div>
</template>""",
        "types.ts.j2": """export interface {{ entity }} {
  id: number;
  name: string;
  description?: string;
  status: 'active' | 'inactive';
  createdAt?: string;
  updatedAt?: string;
}

export interface {{ entity }}ListParams {
  page?: number;
  pageSize?: number;
  search?: string;
  status?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}""",
        "style.vue.j2": """<style>
.{{ entity_lower }}-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.{{ entity_lower }}-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

@media (max-width: 768px) {
  .{{ entity_lower }}-grid {
    grid-template-columns: 1fr;
  }
}
</style>""",
        "page-list.vue.j2": """<template>
  <div class="{{ entity_lower }}-list-page">
    <div class="page-header">
      <h2>{{ entity }}列表</h2>
      <router-link to="/{{ entity_lower }}s/create" class="btn-primary">
        新建
      </router-link>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="items.length === 0" class="empty">
      暂无数据
    </div>
    <div v-else class="list">
      <div v-for="item in items" :key="item.id" class="list-item">
        <router-link :to="`/{{ entity_lower }}s/${item.id}`">
          {{ item.name }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { {{ entity_lower }}Api } from './api';
import type { {{ entity }} } from './types';

const items = ref<{{ entity }}[]>([]);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  items.value = await {{ entity_lower }}Api.list();
  loading.value = false;
});
</script>""",
    },
    "sql": {
        "schema.sql.j2": """-- {{ entity }} Schema
CREATE TABLE IF NOT EXISTS {{ entity_lower }}s (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_{{ entity_lower }}s_name ON {{ entity_lower }}s(name);
CREATE INDEX idx_{{ entity_lower }}s_status ON {{ entity_lower }}s(status);
CREATE INDEX idx_{{ entity_lower }}s_created_at ON {{ entity_lower }}s(created_at);""",
        "crud.sql.j2": "-- {{ entity }} CRUD Operations\n\n-- Create\nINSERT INTO {{ entity_lower }}s (name, description)\nVALUES ('name', 'description')\nRETURNING *;\n\n-- Read\nSELECT * FROM {{ entity_lower }}s WHERE id = 1;\nSELECT * FROM {{ entity_lower }}s WHERE status = 'active' ORDER BY created_at DESC;\n\n-- Update\nUPDATE {{ entity_lower }}s\nSET name = 'new_name', updated_at = NOW()\nWHERE id = 1;\n\n-- Delete\nDELETE FROM {{ entity_lower }}s WHERE id = 1;",
        "index.sql.j2": "-- {{ entity }} Indexes\n\n-- Primary lookup\nCREATE INDEX idx_{{ entity_lower }}s_name ON {{ entity_lower }}s(name);\n\n-- Status queries\nCREATE INDEX idx_{{ entity_lower }}s_status_created\n    ON {{ entity_lower }}s(status, created_at DESC);\n\n-- Full text search\nALTER TABLE {{ entity_lower }}s ADD COLUMN search_vector tsvector;\nCREATE INDEX idx_{{ entity_lower }}s_search ON {{ entity_lower }}s USING GIN(search_vector);\n\n-- Unique constraint\nALTER TABLE {{ entity_lower }}s ADD CONSTRAINT uq_{{ entity_lower }}s_name UNIQUE(name);",
        "migration.sql.j2": "-- {{ entity }} Migration V001\n-- Description: Create {{ entity_lower }}s table\n\n-- Up\nCREATE TABLE {{ entity_lower }}s (\n    id BIGSERIAL PRIMARY KEY,\n    name VARCHAR(255) NOT NULL,\n    description TEXT,\n    created_at TIMESTAMP DEFAULT NOW()\n);\n\n-- Down\n-- DROP TABLE IF EXISTS {{ entity_lower }}s;",
        "function.sql.j2": "-- {{ entity }} Functions\n\nCREATE OR REPLACE FUNCTION update_{{ entity_lower }}_updated_at()\nRETURNS TRIGGER AS $$\nBEGIN\n    NEW.updated_at = NOW();\n    RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql;\n\nCREATE TRIGGER trg_{{ entity_lower }}s_updated_at\n    BEFORE UPDATE ON {{ entity_lower }}s\n    FOR EACH ROW\n    EXECUTE FUNCTION update_{{ entity_lower }}_updated_at();",
    },
    "python": {
        "model.py.j2": """from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class {{ entity }}(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: str = Field(default="active", pattern="^(active|inactive)$")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True""",
        "service.py.j2": """from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.{{ entity_lower }} import {{ entity }}Repository
from models.{{ entity_lower }} import {{ entity }}

class {{ entity }}Service:
    def __init__(self, repo: {{ entity }}Repository):
        self.repo = repo

    async def list(self, session: AsyncSession) -> List[{{ entity }}]:
        return await self.repo.find_all(session)

    async def get(self, session: AsyncSession, id: int) -> Optional[{{ entity }}]:
        return await self.repo.find_by_id(session, id)

    async def create(self, session: AsyncSession, data: dict) -> {{ entity }}:
        return await self.repo.save(session, {{ entity }}(**data))""",
        "api.py.j2": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.{{ entity_lower }} import {{ entity }}Service
from schemas.{{ entity_lower }} import {{ entity }}Create, {{ entity }}Response
from database import get_session

router = APIRouter(prefix="/api/v1/{{ entity_lower }}s", tags=["{{ entity_lower }}"])

@router.get("/", response_model=list[{{ entity }}Response])
async def list_{{ entity_lower }}s(
    service: {{ entity }}Service = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await service.list(session)

@router.post("/", response_model={{ entity }}Response, status_code=201)
async def create_{{ entity_lower }}(
    data: {{ entity }}Create,
    service: {{ entity }}Service = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await service.create(session, data.model_dump())""",
        "test.py.j2": """import pytest
from unittest.mock import AsyncMock
from services.{{ entity_lower }} import {{ entity }}Service
from models.{{ entity_lower }} import {{ entity }}

@pytest.fixture
def service():
    repo = AsyncMock()
    return {{ entity }}Service(repo)

@pytest.mark.asyncio
async def test_create_{{ entity_lower }}(service):
    service.repo.save.return_value = {{ entity }}(id=1, name="test")
    result = await service.create(None, {"name": "test"})
    assert result.name == "test"
    assert result.id == 1""",
        "config.py.j2": """from pydantic_settings import BaseSettings

class {{ entity }}Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://localhost:5432/{{ entity_lower }}"
    debug: bool = False
    log_level: str = "INFO"
    api_prefix: str = "/api/v1/{{ entity_lower }}s"
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = {"env_prefix": "{{ entity_lower.upper() }}_"}

settings = {{ entity }}Settings()""",
    },
}

def safe_write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def main():
    total = 0
    created = 0
    skipped = 0
    for lang, templates in TEMPLATES.items():
        lang_dir = CODE / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        for fname, content in templates.items():
            fp = lang_dir / fname
            total += 1
            if fp.exists():
                skipped += 1
                continue
            safe_write(fp, content)
            created += 1
    print(f"Templates: {total} defined, {created} created, {skipped} skipped")

if __name__ == "__main__":
    main()
