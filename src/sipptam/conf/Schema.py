#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    conf.Schema
    ~~~~~~~~~~~

    Contains a basic XML schema to parse the input configuration file.

    :copyright: (c) 2013 by luismartingil.
    :license: See LICENSE_FILE.
"""

import StringIO

schema = StringIO.StringIO('''\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
    <xs:element name="sipptam">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="tasList" type="tasListType" maxOccurs="1"/>
                <xs:element name="testrunList" type="testrunListType" maxOccurs="1"/>
            </xs:sequence>
            <xs:attribute name="dutHost" type="IPType" use="required"/>
            <xs:attribute name="dutPort" type="xs:positiveInteger" use="required"/>
            <xs:attribute name="logLevel" type="logLevelType" use="required"/>
            <xs:attribute name="logColor" type="xs:string" use="required"/>
        </xs:complexType>
    </xs:element>

    <xs:complexType name="tasListType">
        <xs:sequence>
            <xs:element name="tas" type="tasType" maxOccurs="unbounded"/>        
        </xs:sequence>
    </xs:complexType>

    <xs:complexType name="tasType">
        <xs:attribute name="host" type="IPType" use="required"/>
        <xs:attribute name="port" type="xs:string" use="required"/>
        <xs:attribute name="jobs" type="xs:positiveInteger" use="required"/>
    </xs:complexType>

    <xs:complexType name="testrunListType">
        <xs:sequence>
            <xs:element name="testrun" type="testrunType" maxOccurs="unbounded"/>
        </xs:sequence>
        <xs:attribute name="scenariosPath" type="xs:string" use="required"/>
        <xs:attribute name="scenarioMaxN" type="xs:positiveInteger" use="required"/>
        <xs:attribute name="scenarioMaxSize" type="xs:positiveInteger" use="required"/>
        <xs:attribute name="validateScenarioXML" type="myBoolType" use="required"/>
    </xs:complexType>

    <xs:complexType name="testrunType">
        <xs:sequence>
            <xs:element name="modificationList" type="modificationListType" minOccurs="0" maxOccurs="1"/>
        </xs:sequence>
        <xs:attribute name="applyRegex" type="xs:string" use="required"/>
        <xs:attribute name="pause" type="positiveFloat" use="required"/>
        <xs:attribute name="paramR" type="numberListType" use="required"/>
        <xs:attribute name="paramM" type="numberListType" use="required"/>
        <xs:attribute name="execMode" type="execModeType" use="required"/>
        <xs:attribute name="tries" type="xs:positiveInteger" use="required"/>
    </xs:complexType>

    <xs:complexType name="modificationListType">
        <xs:sequence>
            <xs:element name="replaceList" type="replaceListType" maxOccurs="unbounded"/>        
        </xs:sequence>
    </xs:complexType>

    <xs:complexType name="replaceListType">
        <xs:sequence>
            <xs:element name="replace" type="replaceType" maxOccurs="unbounded"/>        
        </xs:sequence>
        <xs:attribute name="applyRegex" type="xs:string" use="required"/>
        <xs:attribute name="fieldsFile" type="xs:string"/>
    </xs:complexType>

    <xs:complexType name="replaceType">
        <xs:attribute name="src" type="xs:string" use="required"/>
        <xs:attribute name="dst" type="xs:string" use="required"/>
    </xs:complexType>

    <xs:simpleType name="numberListType">
       <xs:restriction base="xs:string">
          <xs:pattern value="([0-9]*)((;[0-9]+)*)?"/>
       </xs:restriction>
    </xs:simpleType>

    <xs:simpleType name="execModeType">
        <xs:restriction base="xs:string">
            <xs:enumeration value="serial"/>
            <xs:enumeration value="parallel"/>
        </xs:restriction>
    </xs:simpleType>

    <xs:simpleType name="IPType">
       <xs:restriction base="xs:string">
          <xs:pattern value="(([1-9]?[0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"/>
       </xs:restriction>
    </xs:simpleType>

    <xs:simpleType name="anyOrIPType">
       <xs:restriction base="xs:string">
          <xs:pattern value="((([1-9]?[0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]))|(\*)"/>
       </xs:restriction>
    </xs:simpleType>

    <xs:simpleType name="logLevelType">
        <xs:restriction base="xs:string">
            <xs:enumeration value="debug"/>
            <xs:enumeration value="info"/>
            <xs:enumeration value="warning"/>
            <xs:enumeration value="error"/>
            <xs:enumeration value="critical"/>
        </xs:restriction>
    </xs:simpleType>

    <xs:simpleType name="positiveFloat">
        <xs:restriction base="xs:float">
            <xs:minInclusive value="0.0"/>
        </xs:restriction>
    </xs:simpleType>

    <xs:simpleType name="myBoolType">
        <xs:restriction base="xs:string">
            <xs:enumeration value="True"/>
            <xs:enumeration value="False"/>
        </xs:restriction>
    </xs:simpleType>

</xs:schema>
''')
